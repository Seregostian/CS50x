def height_input() -> int:
  while True:
    try:
      height = int(input("Height: "))

      if height > 0 and height < 9:
        return height

    except ValueError:
      print("Height has to be between 1 and 8, try again!.")

#code was explained to me by a friend, a more through explanation is in the link below:
#https://www.youtube.com/watch?v=v5WclqvC5To&ab_channel=BlendSec

def pyramid_size(height: int):
  for line in range(height):
    print(" " * (height - line - 1), end="")
    print("#" * (line + 1))

pyramid_size(height_input())