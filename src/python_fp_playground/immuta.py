from pydantic import BaseModel


class ImmutableModel(BaseModel):
    class Config:
        frozen = True


class Emp(ImmutableModel):
    name: str

    class Config:
        frozen = False


emp = Emp(name="Jai Ganesh")
print(emp)
emp.name = "Nope"
print(emp)
