from sqlmodel import SQLModel, Field, create_engine, Session, select

# 1. Define a model
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None

# 2. Create engine (SQLite file db) and tables
engine = create_engine("sqlite:///heroes.db", echo=True)
SQLModel.metadata.create_all(engine)

# 3. Insert some rows
def create_heroes():
    with Session(engine) as session:
        hero_1 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador", age=15)
        hero_2 = Hero(name="Captain North America", secret_name="Mary Canada", age=30)
        hero_3 = Hero(name="Wonder Woman", secret_name="Diana Prince", age=28)

        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.commit()

# 4. Query rows
def list_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.age >= 18).order_by(Hero.age)
        results = session.exec(statement).all()
        for hero in results:
            print(hero.id, hero.name, hero.age)

if __name__ == "__main__":
    create_heroes()
    list_heroes()
    