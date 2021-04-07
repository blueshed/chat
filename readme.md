# Realtime Chat Persisted

<p align="center">
  <img alt="chat package" src="images/two-windows-2.jpg" width="800">
</p>

This article is the third in the series [Realtime Chat with Vite, Vue3 and Python
Tornado](https://pspddo.medium.com/realtime-chat-with-vite-vue3-and-python-tornado-31c8085253af).
In this article we'll add SQLAlchemy persistence and authentication to our chat app.

Since so many changes will be made in this refactor, I've decided to use a different
style. All the source is on the git repo and I'm going to discuss the changes and
motivations while uses clips of code. If you want to see the whole code base - it's
there a working under branch called [article3a](https://github.com/blueshed/chat/tree/article3a) - there is an [article3](https://github.com/blueshed/chat/tree/article3) - but it gave my proof readers a headache.

So tooling up, we need to add [alembic](https://alembic.sqlalchemy.org/en/latest/)
to our `dev.txt` and [sqlalchemy](https://docs.sqlalchemy.org/en/14/) to our
`requirements.txt`. (NB. At the time of writing SQLAlchemy 1.4.0b3 was in beta
and so the actual entry in `requirements.txt` was `sqlalchemy==1.4.0b3`).

Having done that, we can call `make setup` to install the new packages.

## SQLAlchemy

This package supports two flavours of persistence: an object relational mapper
and an expression language. We'll use the expression language. 




The source is on [https://github.com/blueshed/chat/tree/article3
](https://github.com/blueshed/chat/tree/article3a)
