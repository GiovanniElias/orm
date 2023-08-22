# What - A simple orm
---

Il progetto ha lo scopo di implementare le funzionalità base per l'interazione con un database, in maniera intuitiva.
L'utilizzo nel codice è simile a orm popolari, come sqlalchemy.

### A couple of examples:

Instantiate a DB object:

```python
    connection_info = {
        'host': 'localhost',
        'database': 'postgres',
        'user': '*****',
        'password': '*****',
    }
    engine = create_engine(connection_info)
    db = dbsession(engine=engine, autocommit=True)
```

Declare a table object:

```python
    Table = table_base()
    class User(Table):
        id = Column(type=Integer(), name='id', primary_hey=True)
        test = Column(
            type=String(),
            name='test',
            default='default',
            nullable=True
        )
```

Statements:

```python
    ## create

    db.create(User)

    ## select

    db.select(
        table=User,
        columns=[User.id, User.test],
        conditions=[User.id == 'id'],
        group_by=[User.id],
        order_by=[User.id],
        ascending_order=False
    )

    ## update

    db.update(
        table=User,
        set_columns=[User.id == 'new_id']
        conditions=[User.id == 'id']
    )
```


# Why - the goal

My choice to develop a Python ORM aimed to bridge the gap between object-oriented programming and databases; in the perspective of learning by doing, developing this project provided a hands-on understanding of how data is stored and retrieved, deepening comprehension of object-oriented principles and class design.

# How - under the hood

sequenceDiagram
    participant User
    participant Database
    participant Table
    participant Engine
    participant QueryBuilder
    participant ActualDatabase

    User ->> Table: Create Table

    User ->> Database: Execute Operation
    Database ->> Engine: Execute Operation
    Engine ->> QueryBuilder: Prepare Statement
    QueryBuilder ->> Engine: Statement
    Engine ->> ActualDatabase: Execute Statement
    ActualDatabase -->> Engine: Result
    Engine -->> Database: Result
    Database -->> User: Result
