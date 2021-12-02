**IF(direct)**
---
title: "Documentation: Upgrading and downgrading"
description: "Changing your plan by upgrading or downgrading can be done through your account."
---
**ENDIF**

## Upgrading and downgrading

Changing your plan, either by upgrading or downgrading, can be done easily at
any time through
**IF(direct)**
your [account](https://www.memcachier.com/caches) and it Just Works™.
**ENDIF**
**IF(heroku)**
Heroku.
**ENDIF**

  - No code changes are required.
  - Your cache won't be lost or reset<strong>*</strong>.
  - You are charged by the hour for plans, so try experimenting with
    different cache sizes with low cost.

**IF(direct)**
<p class="alert alert-info">
<strong>*</strong> When moving between the development plan to a
production plan, you <strong>will</strong> loose your cache. This is
unavoidable due to the strong separation between the development and
production clusters.
</p>
**ENDIF**

**IF(heroku)**
>note
><strong>*</strong> When moving between the development plan to a
>production plan, you __will__ loose your cache. This is unavoidable
>due to the strong separation between the development and production
>clusters.
**ENDIF**
