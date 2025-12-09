# Define a helper function that prompts the user for an integer choice.
# The user's choice must be between minval and maxval. If the argument loop is set to True,
# the user will provide a list of integers until they type 'end', and the function will return this list of integers.

def integer_choice(prompt, minval, maxval, loop=False):
  integer_choice_list = []
  if not loop:
   while True:
    try:
      value = int(input(prompt))
      if value < minval or value > maxval:
        print(f'Please enter a number between {minval} and {maxval}.')
        continue
      return value
    except ValueError:
      print('Invalid Entry.')
  else:
    while True:
      userinput = input(f'{prompt} \n Type "end" if finished. \n').strip()
      if userinput.lower() == 'end':
        return sorted(integer_choice_list)
      else:
        try:
          value = int(userinput)
          if value < minval or value > maxval:
            print(f'Please enter a number between {minval} and {maxval}.')
            continue
          if value in integer_choice_list:
            continue
          else:
              integer_choice_list.append(value)
        except ValueError:
          print('Invalid Entry.')

# Print list prints enumerated lists so that users can enter an integer that corresponds to an entry in a list.

def print_list(itemlist,item="item"):
  print(f"List of {item if item.endswith('s') else item + 's'}:")
  for i, itemname in enumerate(itemlist, start=1):
    print(f'{i}: {itemname}')

# Safe run is for debugging and testing stuff, honestly chat gpt wrote this part so i dont really know it super well but yeah. if it errors it'll print an error message.

def safe_run(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"An error occurred: {type(e).__name__} – {e}")
        return None
    
