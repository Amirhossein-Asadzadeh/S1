def main(args):
      name = args.get("name", "stranger")
      greeting = "Helloooooooo" + name + "!"
      print(greeting)
      return {"body": greeting}
  
