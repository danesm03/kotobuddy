from sqlmodel import create_engine

engine = create_engine("sqlite:////Users/Dane/bootdev_work/kotobuddy/data/cards.db")
texts_engine = create_engine("sqlite:////Users/Dane/bootdev_work/kotobuddy/data/texts.db")