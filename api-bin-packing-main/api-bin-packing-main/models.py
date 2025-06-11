import pickle
from typing import List, Tuple
from sqlalchemy import ForeignKey, Integer, LargeBinary, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from packing_layer import Packer
import dill

class Base(DeclarativeBase):
     pass

class GartmentTable(Base):
    __tablename__ = "gartment_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    width: Mapped[int] = mapped_column(Integer)
    height: Mapped[int] = mapped_column(Integer)
    bin_maxrects: Mapped[str] = mapped_column(String(5000), nullable=True)
    bin_skyline: Mapped[str] = mapped_column(String(5000), nullable=True)
    bin_guillotine: Mapped[str] = mapped_column(String(5000), nullable=True)

    packers: Mapped[List["PackerModel"]] = relationship(
        "PackerModel", back_populates="table", cascade="all, delete-orphan"
    )

    # (bin_number,x, y, WIDTH, HEIGHT, ID)
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.max_rects_array: List[Tuple[int, int, int, int, int, str]] = None
        self.skyline_array: List[Tuple[int, int, int, int, int, str]] = None
        self.guillotine_array: List[Tuple[int, int, int, int, int, str]] = None


class Shirt(Base):
    __tablename__ = "shirt"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(50))
    size: Mapped[str] = mapped_column(String(3)) # pp p m g gg

    shirt_rects: Mapped[List["ShirtRects"]] = relationship(
        "ShirtRects", back_populates="shirt", cascade="all, delete-orphan"
    )

class ShirtRects(Base):
    __tablename__ = "shirt_rects"

    id: Mapped[int] = mapped_column(primary_key=True)
    width: Mapped[int] = mapped_column(Integer)
    height: Mapped[int] = mapped_column(Integer)
    shirt_id: Mapped[str] = mapped_column(ForeignKey("shirt.id"))

    shirt: Mapped["Shirt"] = relationship("Shirt", back_populates="shirt_rects")

class PackerModel(Base):
    __tablename__ = 'packers'
    id: Mapped[int] = mapped_column(primary_key=True)
    state_max: Mapped[bytes] = mapped_column(LargeBinary)
    state_sky: Mapped[bytes] = mapped_column(LargeBinary)
    state_gui: Mapped[bytes] = mapped_column(LargeBinary)
    table_id: Mapped[int] = mapped_column(ForeignKey("gartment_table.id"))

    # Make sure this matches the relationship in GartmentTable
    table: Mapped["GartmentTable"] = relationship("GartmentTable", back_populates="packers")

    def __init__(self, packer_instance: Packer):
        self.state_max = dill.dumps(packer_instance.get_packer_max())
        self.state_sky = dill.dumps(packer_instance.get_packer_sky())
        self.state_gui = dill.dumps(packer_instance.get_packer_gui())