from sqlalchemy import create_engine, Integer, String, Boolean, Numeric, ForeignKey, select, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, relationship, mapped_column, selectinload
from pathlib import Path

BASE_DIR = Path(__file__).parents[2]
print(__file__)
print(BASE_DIR)

engine = create_engine(
    url=f"sqlite:///{BASE_DIR / 'my_database.db'}"
)


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True
    )


class Category(Base):
    __tablename__ = 'Category'

    name: Mapped[str] = mapped_column(
        String(100), nullable=True)
    description: Mapped[str] = mapped_column(
        String(255), nullable=True)

    products = relationship("Products", back_populates="category")


class Products(Base):
    __tablename__ = 'Product'

    name: Mapped[str] = mapped_column(
        String(100), nullable=False)
    price: Mapped[Numeric] = mapped_column(
        Numeric(), nullable=True)
    is_stock: Mapped[bool] = mapped_column(
        Boolean, default=True)
    # categories: Mapped[str] = mapped_column(
    #     String(25), nullable=True)

    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Category.id"),
        nullable=True
    )

    category = relationship("Category", back_populates="products")


Base.metadata.create_all(bind=engine)

Session = sessionmaker(
    bind=engine
)

session = Session()

Base.metadata.drop_all(bind=engine)

Base.metadata.create_all(bind=engine)

electronics = Category(name='Electronics', description='Gadgets and devices')
books = Category(name='Books', description='Printed books and e-books')
clothing = Category(name='Clothing', description='Clothing for men and women')

session.add_all([electronics, books, clothing])
session.commit()

session.add_all([Products(name='Smartphone', price=299.99, is_stock=True, category=electronics),
                 Products(name='Laptop', price=499.99, is_stock=True, category=electronics),
                 Products(name='Science fiction novel', price=15.99, is_stock=True, category=books),
                 Products(name='Jeans', price=40.50, is_stock=True, category=clothing),
                 Products(name='T-shirt', price=20.00, is_stock=True, category=clothing)
                 ])
session.commit()

stmt = select(Category).options(selectinload(Category.products))
categories = session.scalars(stmt).all()

for c in categories:
    print(c.id, c.name, c.description)
    for p in c.products:
        print(p.name, p.price)

product = session.get(Products, 1)
if Products:
    product.price = 349.99
    session.commit()
    product = session.get(Products, 1)
    print(product.name, product.price)

session.commit()

stmt = (
    select(
        Category.name,
        func.count(Products.id)
    )
    .join(Products)
    .group_by(Category.id)
)

result = session.execute(stmt)

for name, count in result:
    print(f"{name}: {count}")

session.commit()

stmt = (
    select(
        Category.name,
        func.count(Products.id)
    )
    .join(Products)
    .group_by(Category.id)
    .having(func.count(Products.id) > 1)

)

result = session.execute(stmt)

for name, count in result:
    print(f"Категория, в которых более одного продукта: {name}: {count}")

session.commit()
