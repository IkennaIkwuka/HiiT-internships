class Dog:
    # Class attribute
    species = "Canis Familaris"

    # Initializer / Instance attributes
    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age

    # Instance method
    def description(self):
        return f"{self.name} is {self.age} years old."


# Creating objects (instances) of the Dog class
my_dog = Dog("Buddy", 5)
your_dog = Dog("Lucy", 3)

# Accessing attributes and calling methods
print(my_dog.description())
print(f"{your_dog.name} is a {Dog.species}")
