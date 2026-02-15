from sqlalchemy import create_engine, BigInteger, String, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, relationship, mapped_column
from pathlib import Path

BASE_DIR = Path(__file__).parents[2]
print(__file__)
print(BASE_DIR)

engine = create_engine(
    url=f"sqlite:///:memory:"
)


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        BigInteger,
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
        Boolean, default=True
    )
    category_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("Category.id"),
        nullable=True
    )

    category = relationship("Category", back_populates="products")


Base.metadata.create_all(bind=engine)

Session = sessionmaker(
    bind=engine
)

# session = Session()
