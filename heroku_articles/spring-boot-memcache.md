

Memcache is a technology that improves the performance and scalability of web
apps and mobile app backends. You should consider using Memcache when your pages
are loading too slowly or your app is having scalability issues. Even for small
sites, Memcache can make page loads snappy and help future-proof your app.

This guide shows how to create a simple
[Spring Boot 2](https://projects.spring.io/spring-boot/) application (based on
the [Spring Framework 5](https://spring.io/)), deploy it to Heroku, then add
Memcache to alleviate a performance bottleneck.

>note
>The sample app in this guide can be seen running
>[here](https://memcachier-examples-spring.herokuapp.com/). You can
>[view the source code](https://github.com/memcachier/examples-spring-boot)
>or deploy it with this Heroku Button:
>
>[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/memcachier/examples-spring-boot)

## Prerequisites
Before you complete the steps in this guide, make sure you have all of the
following:

* Familiarity with Java (and ideally Spring Boot)
* A Heroku user account
([signup is free and instant](https://signup.heroku.com/signup/dc))
* Maven, and the [Heroku CLI](heroku-cli) installed on your computer

## Deploying a Spring Boot application to Heroku

To easily create a Spring Boot application we recommend you to install the
[Spring Boot CLI](https://docs.spring.io/spring-boot/docs/current/reference/html/getting-started-installing-spring-boot.html#getting-started-installing-the-cli).
If you don't want to install the CLI you can also configure and download a
Spring Boot skeleton from the [Spring Initializer](http://start.spring.io/).

> note
> There is a ruby on rails application called spring as well. In case you have it
> installed or in case you have the Ruby version manager `rbenv` installed which
> shims this binary, create an alias for the spring cli (e.g.,
> `alias springboot='/opt/spring-boot-cli/bin/spring'`).

With the CLI you can easily create a skeleton:

```term
$ spring init --d=web,data-jpa,thymeleaf -g com.memcachier -a tutorial -n TaskList memcached_tutorial
$ cd memcached_tutorial
```

The created skeleton is a web app with database support (`data-jpa`) and using
the `thymeleaf` template language. Spring Boot also supports other template
languages such as JSP, groovy, freemaker, and mustache.

### Create a Heroku app

Turning the Spring Boot skeleton into a Heroku app is easily done with 3 simple
steps:

1. In order to let Heroku know how to start up your app, you need to add a
  [`Procfile`](procfile):

  ```term
  $ echo 'web: java -Dserver.port=$PORT $JAVA_OPTS -jar target/*.jar' > Procfile
  ```

2. Initialize a Git repository and commit the skeleton:

  ```term
  $ git init
  $ git add .
  $ git commit -m 'Spring Boot skeleton for Heroku'
  ```

3. Create a Heroku app:

  ```term
  $ heroku create
  ```

  In addition to creating the actuall Heroku application this command also adds
  the corresponding remote to your local Git repository.

## Add task list functionality

Let's add a task list to the app that enables users to view, add, and delete
tasks. To accomplish this, we need to:

1. Set up the database
2. Create a `Task` entity and a table to store them
3. Create the view and controller logic

### Set up a PostgreSQL database

Before we can configure a database in Spring Boot, we need to create the
database. On Heroku, you can add a free development database to your app like
so:

```term
$ heroku addons:create heroku-postgresql:hobby-dev
```

This creates a PostgreSQL database for your app and adds a `DATABASE_URL` config
var that contains its URL.

>note
>Spring Boot requires the variable `SPRING_DATASOURCE_URL` to be set. This
>variable contains the same URL as `DATABASE_URL` except that it starts with
>`jdbc:postgresql` instead of `postgres`. Heroku will automatically populate
>this variable at runtime so you don't have to worry about it.

To use this database we need to install a few packages. Add the following
dependencies in `pom.xml`:

```xml
<dependency>
  <groupId>org.postgresql</groupId>
  <artifactId>postgresql</artifactId>
</dependency>
<dependency>
  <groupId>javax.xml.bind</groupId>
  <artifactId>jaxb-api</artifactId>
  <version>2.3.0</version>
</dependency>
<dependency>
  <groupId>org.liquibase</groupId>
  <artifactId>liquibase-core</artifactId>
  <version>3.6.1</version>
</dependency>
```

* The first dependency simply is the PostgreSQL driver.

* The second dependency just adds the JAXB APIs, as they are no longer
  available out of the box for newer Java SE versions. For more information see
  [this Stack Overflow thread](https://stackoverflow.com/questions/43574426/how-to-resolve-java-lang-noclassdeffounderror-javax-xml-bind-jaxbexception-in-j).

* The third dependency allows you to create and run liquibase database migrations.

Now we can configure the database in `src/main/resources/application.properties`:

  ```properties
  spring.datasource.driverClassName=org.postgresql.Driver
  spring.datasource.maxActive=10
  spring.datasource.maxIdle=5
  spring.datasource.minIdle=2
  spring.datasource.initialSize=5
  spring.datasource.removeAbandoned=true

  # Supress exception regarding missing PostgreSQL CLOB feature at Spring startup.
  # See http://vkuzel.blogspot.ch/2016/03/spring-boot-jpa-hibernate-atomikos.html
  spring.jpa.properties.hibernate.temp.use_jdbc_metadata_defaults = false
  spring.jpa.database-platform=org.hibernate.dialect.PostgreSQL9Dialect
  ```

Your PostgreSQL database is now ready to be used. Save the changes with

```term
$ git commit -am 'Database setup'
```

For more info on connecting to relational databases from Java on Heroku, see
[this guide](connecting-to-relational-databases-on-heroku-with-java).


### Create the Task entity and database table

In order to create and store tasks we need to create three things: a `Task`
entity, a repository to teach Spring Boot how to store and retrieve tasks, and
a migration that creates the actual table in the database.

1. Add the `Task` entity to `src/main/java/com/memcachier/tutorial/Task.java`:

  ```java
  package com.memcachier.tutorial;

  import javax.persistence.Entity;
  import javax.persistence.GeneratedValue;
  import javax.persistence.GenerationType;
  import javax.persistence.Id;

  import org.hibernate.validator.constraints.NotEmpty;

  @Entity
  public class Task {

    @Id
    @GeneratedValue(strategy=GenerationType.IDENTITY)
    private Long id;
    @NotEmpty
    private String name;

    protected Task() {}

    public Task(String name) {
      this.name = name;
    }

    public Long getId() {
      return this.id;
    }

    public String getName() {
      return this.name;
    }

    public void setName(String name) {
      this.name = name;
    }

    @Override
    public String toString() {
      return String.format("Task[id=%d, name='%s']", this.id, this.name);
    }

  }
  ```

2. Create a repository in `src/main/java/com/memcachier/tutorial/TaskRepository.java`:

  ```java
  package com.memcachier.tutorial;

  import java.util.List;
  import org.springframework.data.repository.CrudRepository;

  public interface TaskRepository extends CrudRepository<Task, Long> {}
  ```

  If you need more than basic CRUD functions to access your data you can
  also extend a `PagingAndSortingRepository` or a `JpaRepository` instead. See
  [this StackOverflow thread](https://stackoverflow.com/questions/14014086/what-is-difference-between-crudrepository-and-jparepository-interfaces-in-spring)
  for more information.

3. Create a liquibase migration in
  `src/main/resources/db/changelog/db.changelog-master.yaml`:

  ```yaml
  databaseChangeLog:
    - changeSet:
        id: 1
        author: memcachier
        changes:
          - createTable:
              tableName: task
              columns:
                - column:
                    name: id
                    type: int
                    autoIncrement: true
                    constraints:
                      primaryKey: true
                      nullable: false
                - column:
                    name: name
                    type: varchar(255)
                    constraints:
                      nullable: false
  ```

  Note, you will need to create the `db` and `changelog` folders.
  The migration will run automatically when the application starts.

Let's save the changes so far:

```term
$ git add .
$ git commit -m 'Task table setup'
```

### Create the task list application

The actual application consists of a view that is displayed in the frontend and
a controller that implements the functionality in the backend.

* Create a controller in `src/main/java/com/memcachier/tutorial/TaskController.java`:

  ```java
  package com.memcachier.tutorial;

  import javax.validation.Valid;
  import java.lang.Iterable;

  import org.springframework.beans.factory.annotation.Autowired;
  import org.springframework.stereotype.Controller;
  import org.springframework.ui.ModelMap;
  import org.springframework.validation.BindingResult;
  import org.springframework.web.bind.annotation.ModelAttribute;
  import org.springframework.web.bind.annotation.RequestMapping;
  import org.springframework.web.bind.annotation.RequestMethod;
  import org.springframework.web.bind.annotation.RequestParam;

  @Controller
  @RequestMapping("/")
  public class TaskController {

    private TaskRepository taskRepo;

    @Autowired
    public TaskController(TaskRepository repo) {
      this.taskRepo = repo;
    }

    @RequestMapping(method = RequestMethod.GET)
    public String showAllTasks(ModelMap model) {
      Iterable<Task> tasks = this.taskRepo.findAll();
      model.addAttribute("tasks", tasks);
      model.addAttribute("newTask", new Task());
      return "task";
    }

    @RequestMapping(method = RequestMethod.POST)
    public String newTask(ModelMap model,
                          @ModelAttribute("newTask") @Valid Task task,
                          BindingResult result) {
      if (!result.hasErrors()) {
        this.taskRepo.save(task);
      }
      return showAllTasks(model);
    }

    @RequestMapping(method = RequestMethod.DELETE)
    public String deleteTask(ModelMap model, @RequestParam("taskId") Long id) {
      this.taskRepo.deleteById(id);
      return showAllTasks(model);
    }
  }
  ```

  This controller contains all functionality to `GET` all tasks and render the
  `task` view, to `POST` a new task that will then be saved to the database,
  and to `DELETE` existing tasks.

* Create a view in `src/main/resources/templates/task.html`:

  ```html
  <!DOCTYPE HTML>
  <html xmlns:th="http://www.thymeleaf.org">
    <head>
      <title>MemCachier Spring Boot Tutorial</title>
      <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />

      <!-- Fonts -->
      <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.4.0/css/font-awesome.min.css"
            rel='stylesheet' type='text/css' />

      <!-- Bootstrap CSS -->
      <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
            rel="stylesheet" />
    </head>

    <body>
      <div class="container">

        <!-- New Task Card -->
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">New Task</h5>

            <form th:object="${newTask}" method="POST">
              <div class="form-group">
                <input type="text" class="form-control"
                       placeholder="Task Name" th:field="*{name}" />
              </div>
              <button type="submit" class="btn btn-default">
                <i class="fa fa-plus"></i> Add Task
              </button>
            </form>
          </div>
        </div>

        <!-- Current Tasks -->
        <div th:if="${not #lists.isEmpty(tasks)}">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Current Tasks</h5>

              <table class="table table-striped">
                <tr th:each="task : ${tasks}">
                  <!-- Task Name -->
                  <td th:text="${task.name}" class="table-text"></td>
                  <!-- Delete Button -->
                  <td>
                    <form th:object="${deleteTask}" th:method="DELETE">
                      <input type="hidden" name="taskId" th:value="${task.id}">
                      <button type="submit" class="btn btn-danger">
                        <i class="fa fa-trash"></i> Delete
                      </button>
                    </form>
                  </td>
                </tr>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Bootstrap related JavaScript -->
      <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"></script>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
      <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
    </body>
  </html>
  ```

  The view basically consists of two cards, one that contains a form to create
  new tasks and another containing a table with the existing tasks and a delete
  button to remove the corresponding task.

Let us see what we have done so far and deploy the task list to Heroku:

```term
$ git add .
$ git commit -m 'Add task list view and controller'
$ git push heroku master
$ heroku open
```

Test the application by adding a few tasks. We now have a functioning task
list running on Heroku. With this complete, we can learn how to improve
its performance with Memcache.

## Add caching to Spring Boot

Memcache is an in-memory, distributed cache. Its primary API consists of two
operations: `SET(key, value)` and `GET(key)`.
Memcache is like a hashmap (or dictionary) that is spread across
multiple servers, where operations are still performed in constant
time.

The most common use for Memcache is to cache expensive database
queries and HTML renders so that these expensive operations don’t
need to happen over and over again.

### Set up Memcache

To use Memcache in Spring Boot, you first need to provision an actual Memcache
cache. You can easily get one for free with the
[MemCachier add-on](https://elements.heroku.com/addons/memcachier):

```term
$ heroku addons:create memcachier:dev
```

Then we need to configure the appropriate dependencies. We will use
[`simple-spring-memcached`](https://github.com/ragnor/simple-spring-memcached)
with [`XMemcached`](https://github.com/killme2008/xmemcached/) to use Memcache
within Spring Boot. You can use also `simple-spring-memcached` with
[`SpyMemcached`](https://github.com/couchbase/spymemcached). If you wish to
do so, please refer to the [MemCachier documentation](memcachier#spring-boot).

To use `simple-spring-memcached` add the following to your `pom.xml`:

```xml
<dependency>
  <groupId>com.google.code.simple-spring-memcached</groupId>
  <artifactId>xmemcached-provider</artifactId>
  <version>4.0.0</version>
</dependency>
<!-- Force XMemcached to version 2.4.3 (simple-spring-memcached uses 2.4.0) -->
<dependency>
  <groupId>com.googlecode.xmemcached</groupId>
  <artifactId>xmemcached</artifactId>
  <version>2.4.3</version>
</dependency>
```

Now we can configure Memcache for Spring in
`src/main/java/com/memcachier/tutorial/MemCachierConfig.java`:

```java
package com.memcachier.tutorial;

import java.net.InetSocketAddress;
import java.util.List;
import java.util.Map;
import java.util.HashMap;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.google.code.ssm.CacheFactory;
import com.google.code.ssm.config.AbstractSSMConfiguration;
import com.google.code.ssm.config.DefaultAddressProvider;
import com.google.code.ssm.providers.xmemcached.XMemcachedConfiguration;
import com.google.code.ssm.providers.xmemcached.MemcacheClientFactoryImpl;
import net.rubyeye.xmemcached.auth.AuthInfo;
import net.rubyeye.xmemcached.utils.AddrUtil;

@Configuration
public class MemCachierConfig extends AbstractSSMConfiguration {

  @Bean
  @Override
  public CacheFactory defaultMemcachedClient() {
    String serverString = System.getenv("MEMCACHIER_SERVERS").replace(",", " ");
    List<InetSocketAddress> servers = AddrUtil.getAddresses(serverString);
    AuthInfo authInfo = AuthInfo.plain(System.getenv("MEMCACHIER_USERNAME"),
                                       System.getenv("MEMCACHIER_PASSWORD"));
    Map<InetSocketAddress, AuthInfo> authInfoMap =
      new HashMap<InetSocketAddress, AuthInfo>();
    for(InetSocketAddress server : servers) {
      authInfoMap.put(server, authInfo);
    }

    final XMemcachedConfiguration conf = new XMemcachedConfiguration();
    conf.setUseBinaryProtocol(true);
    conf.setAuthInfoMap(authInfoMap);

    final CacheFactory cf = new CacheFactory();
    cf.setCacheClientFactory(new MemcacheClientFactoryImpl());
    cf.setAddressProvider(new DefaultAddressProvider(serverString));
    cf.setConfiguration(conf);
    return cf;
  }
}
```

This configures `simple-spring-memcached` which allows you to use its caching
annotations. Spring also provides built in caching annotations that can be
enabled via `simple-spring-memcached`. However, in this tutorial we will use
the annotations provided `simple-spring-memcached` because they are generally
more flexible and better suited for a Memcached backed cache. Nevertheless,
this tutorial would work just as well with Spring's annotations. If you prefer
to use Spring's built in caching annotations, please refer to the
[MemCachier documentation](memcachier/#spring-boot).

### Cache expensive database queries

Memcache is often used to cache expensive database queries. In this simple
example we do not have any expensive queries but for the sake of learning, let's
assume that getting all tasks from the database is an expensive operation.

To cache the Task queries we will extend the `TaskRepository` with methods that
implement caching. Extending a repository in Spring Boot involves three steps:

1. Build an interface with the methods that should be added to the `TaskRepository`
  in `src/main/java/com/memcachier/tutorial/CachedTaskRepository.java`:

  ```java
  package com.memcachier.tutorial;

  import java.lang.Iterable;

  public interface CachedTaskRepository {

    public Iterable<Task> findAllCached();

  }
  ```

2. Create a an implementation for this interface in
  `src/main/java/com/memcachier/tutorial/TaskRepositoryImpl.java`:

  ```java
  package com.memcachier.tutorial;

  import java.lang.Iterable;

  import org.springframework.beans.factory.annotation.Autowired;
  import com.google.code.ssm.api.ReadThroughAssignCache;

  public class TaskRepositoryImpl implements CachedTaskRepository {

    @Autowired
    TaskRepository taskRepository;

    @ReadThroughAssignCache(namespace="Taskrepo", assignedKey="all")
    public Iterable<Task> findAllCached() {
      return this.taskRepository.findAll();
    }
  }
  ```

  >note
  >The filename of the implementation must follow the naming convention
  >`<REPOSITORY-NAME>Impl.java`.

  You can access the rest of the CRUD interface of the `TaskRepository` by just
  adding an `@Autowired` reference to it.

  The caching occurs here via the `@ReadThroughAssignCache` annotation. All
  `@ReadThrough*Cache` annotations do the following:

  * Check if value is in cache and if true return said value.
  * If not in cache, execute function, return its value and store said value in
    the cache.

  The `Assign` version of this annotation will use an assigned key that is
  declared in the annotation. For more information about the annotations,
  refer to the
  [Simple Spring Memcached documentation](https://github.com/ragnor/simple-spring-memcached/wiki/Getting-Started#usage).

3. Make sure this implementation is integrated into the `TaskRepository`.
  This is simply done by making the `TaskRepository` interface also extend the
  `CachedTaskRepository` interface:

  ```java
  // ...
  public interface TaskRepository extends CrudRepository<Task, Long>, CachedTaskRepository {}
  ```

>note
>A note on caching annotations: Spring uses proxies to handle caching
>annotations. For this reason you cannot create a private method inside your
>controller, add a caching annotation and expect the method to be cached. In
>simple terms, the cached method must be part of a component that is accessed
>via it's interface. For more information see
>[this Stackoverflow thread](https://stackoverflow.com/questions/12115996/spring-cache-cacheable-method-ignored-when-called-from-within-the-same-class)
>and the therein mentioned references.

Now we have the methods to cache all tasks but in order for them to work the
Task data type in `src/main/java/com/memcachier/tutorial/Task.java` needs to be
serializable:

```java
// ...
import java.io.Serializable;

public class Task implements Serializable {
  // ...
}
```

Finally, we can now get the cached tasks in the controller in
  `src/main/java/com/memcachier/tutorial/TaskController.java`:

```java
// ...
public String showAllTasks(ModelMap model) {
  Iterable<Task> tasks = this.taskRepo.findAllCached();
  // ...
}
// ...
```

Let us deploy and test this new functionality:

```term
$ git add .
$ git commit -m 'Add caching with MemCachier'
$ git push heroku master
$ heroku open
```

To see what is going on in your cache, open the MemCachier dashboard:

```term
$ heroku addons:open memcachier
```

The first time you loaded your task list you should have gotten an increase for
the get misses and the set commands. Every subsequent reload of the task list
should increase the get hits (refresh the stats in the dashboard).

Our cache is working but there is still a mayor problem. Add a new task and see
what happens. No new task appears on our current tasks list. The new task was
created in our database but our app is serving the stale task list from the
cache.

### Clear stale data

As important as caching data, is to invalidate it when it becomes stale. In our
example the cached task list becomes stale whenever a new task is added or an
existing task is removed. We need to make sure our cache is invalidated
whenever one of these two actions are performed.

We can add wrappers to the save and delete methods in the `TaskRepository`
that clear the cache with the following two steps:

1. Declare the wrapper methods in the `CachedTaskRepository` interface in
  `src/main/java/com/memcachier/tutorial/CachedTaskRepository.java`:

  ```java
  // ...
  public interface CachedTaskRepository {
    public Iterable<Task> findAllCached();
    public Task saveAndClearCache(Task t);
    public void deleteByIdAndClearCache(Long id);
  }
  ```

2. Implement the wrapper methods in
  `src/main/java/com/memcachier/tutorial/TaskRepositoryImpl.java`:

  ```java
  // ...
  import com.google.code.ssm.api.InvalidateAssignCache;

  public class TaskRepositoryImpl implements CachedTaskRepository {
    // ...

    @InvalidateAssignCache(namespace="Taskrepo", assignedKey="all")
    public Task saveAndClearCache(Task t){
      return this.taskRepository.save(t);
    }

    @InvalidateAssignCache(namespace="Taskrepo", assignedKey="all")
    public void deleteByIdAndClearCache(Long id){
      this.taskRepository.deleteById(id);
    }
  }
  ```

  The stale data is invalidated here via `@InvalidateAssignCache` annotation.
  Just as `@ReadThroughAssignCache` it acts on the assigned key that is
  declared in the annotation.


Now we can use these wrapper functions in our controller to clear the cache
whenever a request comes in to add or delete a task. To do so replace `save`
and `deleteById` in `src/main/java/com/memcachier/tutorial/TaskController.java`
with `saveAndClearCache` and `deleteByIdAndClearCache` like so:

```java
// ...
@RequestMapping(method = RequestMethod.POST)
public String newTask(ModelMap model,
                      @ModelAttribute("newTask") @Valid Task task,
                      BindingResult result) {
  if (!result.hasErrors()) {
    this.taskRepo.saveAndClearCache(task);
  }
  return showAllTasks(model);
}

@RequestMapping(method = RequestMethod.DELETE)
public String deleteTask(ModelMap model, @RequestParam("taskId") Long id) {
  this.taskRepo.deleteByIdAndClearCache(id);
  return showAllTasks(model);
}
```

Deploy the fixed task list:

```term
$ git commit -am 'Clear stale data from cache'
$ git push heroku master
$ heroku open
```

Add a new task and you will see all the tasks appear you have added since we
implemented caching for the task list.

## Further reading & resources

* [MemCachier Add-on Page](https://elements.heroku.com/addons/memcachier)
* [MemCachier Documentation](memcachier)
* [Advance Memcache Usage](advanced-memcache)
* [Heroku Spring Boot Guide](https://devcenter.heroku.com/articles/deploying-spring-boot-apps-to-heroku)
* [Simple Spring Memcached Documentation](https://github.com/ragnor/simple-spring-memcached/wiki/Getting-Started)
* [Spring Caching Guide](https://spring.io/guides/gs/caching/)
* [Spring Caching Documentation](https://docs.spring.io/spring/docs/5.0.5.RELEASE/spring-framework-reference/integration.html#cache)
