# The class ResponseData holds the functions that are responsible for telling the model how to read the user's CSV.
import pandas as pd
import numpy as np
from helpers import integer_choice, print_list, safe_run

print("Loading file_reader")

class ResponseData:
  def __init__(self, df: pd.DataFrame):
    self.df = df                  # This dataframe is the one read from the file inputted earlier.ormation.
    self.slot_groups = {
        'Self Directed': [],
        'Directed': []
    }                             # This provides a dictionary where slots are assigned to slot groups.
    self.instrument_groups = {
        'Chord': [],
        'Melody': []
    }                             # Similar to slot groups dictionary, but for instrument groups.
    self.instrument_list = ['Piano','Guitar','Other Chord','Bass','Drums','Other Percussion','Alto Sax','Tenor Sax','Bari Sax','Trombone','Trumpet','Flute','Clarinet','Other Horn','Vox'] # Initialized list of instruments.
    self.available_keyword = 'Yes'                # Keyword in the CSV which signals an individual's availability
    self.unavailable_keyword = 'No'               # Keyword in the CSV which signals an individual's lack of availability
    self.columnslist = self.df.columns.tolist()   # Lists the columns in the CSV - useful for asking users which columns are which (in conjunction with integer_choice and print_list functions)
    self.instr_col = 'Instrument'
    self.name_col = 'Name'
    self.availability_matrix = None
    self.instrumentation_matrix = None
    self.updated_df = None
    self.names_list = list(self.df[self.name_col])


  # Interface for the user to see what has been assigned to what so far.
  # NEXT STEPS: Somehow link the interfaces from the different classes together to create one smooth, continuous UX.
  def view_assignments(self):
    while True:
      assignments_list = [
          'Name Column',
          'Instrument Column',
          'Slot Groups',
          'Instrument Groups',
          'Instrument List',
          'Names List',
          '"Available" Keyword',
          '"Unavailable" Keyword',
          'Back'
      ]
      print_list(assignments_list)
      assignmentnum = integer_choice('Select the number corresponding to the assignment you would like to view/edit.',1,len(assignments_list)) - 1
      assignmentchoice = assignments_list[assignmentnum]

      if assignmentchoice == 'Name Column':
        optionnum = integer_choice(f'The current name column is {self.name_col}. \n If you would like to edit the name column, type "1". If you would like to go back, type "2".',1,2)
        if optionnum == 1:
          self.assign_name_col()
        else:
          continue

      elif assignmentchoice == 'Instrument Column':
        optionnum = integer_choice(f'The current instrument column is {self.instr_col}. \n If you would like to edit the instrument column, type "1". If you would like to go back, type "2".',1,2)
        if optionnum == 1:
          self.assign_instr_col()
        else:
          continue

      elif assignmentchoice == 'Slot Groups':
        print('The current slot groups are as follows:')
        for i, (groupname, slots) in enumerate(self.slot_groups.items(), start=1):
          if len(slots) == 0:
            slots = 'No slots have been assigned.'
          print(f'{i}: {groupname} - {slots}')
        optionnum = integer_choice(f'If you would like to edit the slot groups, type "1". If you would like to go back, type "2".',1,2)
        if optionnum == 1:
          self.edit_slot_groups()
        else:
          continue

      elif assignmentchoice == 'Instrument Groups':
        print('The current instrument groups are as follows:')
        for i, (groupname, instruments) in enumerate(self.instrument_groups.items(), start=1):
          if len(instruments) == 0:
            slots = 'No slots have been assigned.'
          print(f'{i}: {groupname} - {instruments}')
        optionnum = integer_choice(f'If you would like to edit the instrument groups, type "1". If you would like to go back, type "2".',1,2)
        if optionnum == 1:
          self.edit_inst_groups()
        else:
          continue

      elif assignmentchoice == 'Instrument List':
        print('The current instrument list is:')
        print_list(self.instrument_list,'instrument')
        optionnum = integer_choice(f'If you would like to edit the instrument list, type "1". If you would like to go back, type "2".',1,2)
        if optionnum == 1:
          self.edit_instruments()
        else:
          continue

      elif assignmentchoice == 'Names List':
        print_list(self.names_list,'names')
        continue

      elif assignmentchoice == '"Available" Keyword':
        optionnum = integer_choice(f'The current "available" keyword is {self.available_keyword}. \n If you would like to edit the "available" keyword, type "1". If you would like to go back, type "2".',1,2)
        if optionnum == 1:
          self.assign_available_keyword()
        else:
          continue

      elif assignmentchoice == '"Unavailable" Keyword':
        optionnum = integer_choice(f'The current "unavailable" keyword is {self.unavailable_keyword}. \n If you would like to edit the "unavailable" keyword, type "1". If you would like to go back, type "2".',1,2)
        if optionnum == 1:
          self.assign_unavailable_keyword()
        else:
          continue

      elif assignmentchoice == 'Back':
        return

  # Self explanatory -- tool to edit instrument list
  def edit_instruments(self):
    while True:
      print_list(self.instrument_list, 'instrument')
      print_list(['Add Instrument','Delete Instrument','Back'],'options')
      choicenum = integer_choice('Enter the number corresponding to the option you wish to select',1,3)
      if choicenum == 1:
        self.instrument_list.append(str(input('Enter the name of the instrument you would like to add:')).strip())
      elif choicenum == 2:
        print_list(self.instrument_list, 'instrument')
        instrnum = integer_choice('Enter the number corresponding to the instrument you wish to delete.',1,len(self.slot_groups)) - 1
        del self.instrument_list[instrnum]
      else:
        return

# assigns a name column (from self.col list)
# NOTE: FOR EACH OF THESE FUNCTIONS, I NEED TO CODE A WAY FOR THE USER TO GET OUT!!!! I KEEP NOT DOING THIS BECAUSE IT SOUNDS BORING BUT THEN I MAKE A MISTAKE AND
# NEED TO MANUALLY END THE CODE WHICH SUCKS!!!1!!1!1!!1!!
  def assign_name_col(self):
    print_list(self.columnslist,'column')
    namecolumnnum = integer_choice('Enter the number of the column which contains student names: \n',1,len(self.columnslist))
    self.name_col = self.columnslist[namecolumnnum - 1]
    print(f'Name column successfully set to: {self.name_col}')
    self.names_list = list(self.df[self.name_col])

# assigns an intstrument column (from self.col list)
  def assign_instr_col(self):
    print_list(self.columnslist,'column')
    instrcolumnnum = integer_choice('Enter the number of the column which contains instruments: \n',1,len(self.columnslist))
    self.instr_col = self.columnslist[instrcolumnnum - 1]
    print(f'Instrument column successfully set to: {self.instr_col}')

# self explanatory (i hope)
  def assign_available_keyword(self):
    new_available_keyword = str(input('Enter the value which a cell takes if a given student is available at a given time (EX: "Yes"): \n'))
    self.available_keyword = new_available_keyword
    print(f'Available Keyword successfully set to: {self.available_keyword}')

  def assign_unavailable_keyword(self):
    new_unavailable_keyword = str(input('Enter the value which a cell takes if a given student is unavailable at a given time (EX: "No"): \n'))
    self.unavailable_keyword = new_unavailable_keyword
    print(f'Unavailable Keyword successfully set to: {self.unavailable_keyword}')

# reassigns the slots in a chosen slot group.
# CURRENT DRAWBACKS: Doesn't allow for small-scale editing. Just rewriting everything.
# Also, somehow find a way to exclude name + instr col and all that, and like raise a warning if the column has entries other than the assigned keywords.
# Also Also, slots NEED to be assigned for the creation of sets and parameters and constraints to go smoothly in the scheduling model phase -- so put checks
# on the user to make sure that everything that they need to be defined is defined before the modeling object is created.
  def reassign_slots(self):
    self.times_list = [slot for group in self.slot_groups.values() for slot in group]
    print_list(list(self.slot_groups.keys()),'slot group')
    groupnum = integer_choice('Enter the number which corresponds to the slot group you wish you edit.',1,len(self.slot_groups))
    groupchoice = list(self.slot_groups.keys())[groupnum-1]
    self.slot_groups[groupchoice] = []
    print_list(self.columnslist,'column')
    print('NOTICE: Only select columns which contain only the un/available keywords. For example, do NOT choose the Name column.')
    slotnums = integer_choice(f"Enter the number of a slot you wish to assign to {groupchoice}: \n",1,len(self.columnslist),True)
    for num in slotnums:
      slotchoice = self.columnslist[num-1]
      if slotchoice not in self.times_list:
        self.slot_groups[groupchoice].append(slotchoice)
      else:
        print(f'{slotchoice} has already been assigned to a slot group. It has not been added to the following group: {groupchoice}.')
    print(f'The following have been assigned to {groupchoice}:')
    for slot in self.slot_groups[groupchoice]:
      print(slot)
    self.times_list = [slot for group in self.slot_groups.values() for slot in group]

# edits the slot groups themselves.
  def edit_slot_groups(self):
    while True:
      print_list(['Add Slot Group', 'Remove Slot Group', 'Reassign Slot Group','Back'], 'choices')
      choicenum = integer_choice('Select the number corresponding to the option you would like.',1,4)
      if choicenum == 1:
        self.slot_groups[str(input('Enter the name of the slot group you would like to create:'))] = []
      elif choicenum == 2:
        print_list(list(self.slot_groups.keys()), 'slot groups')
        groupnum = integer_choice('Enter the number corresponding to the slot group you wish to delete.',1,len(self.slot_groups))
        groupchoice = list(self.slot_groups.keys())[groupnum-1]
        del self.slot_groups[groupchoice]
      elif choicenum == 3:
        self.reassign_slots()
      else:
        return

# build the availability matrix that the SchedulingModel will then use to build a parameter -- THIS IS VERY IMPORTANT TO CALL BEFORE CREATING A SCHEDULING MODEL OBJECT!!!
# TO DO: Ensure the user has run this code before creading the rest of SchedulingModel object!!
  def build_availability_matrix(self):
    self.times_list = [slot for group in self.slot_groups.values() for slot in group]
    matrix_columns = self.times_list
    self.availability_matrix = pd.DataFrame(index=np.arange(len(self.df[self.name_col])),columns=matrix_columns)
    # self.availability_matrix[self.name_col] = self.df[self.name_col]
    # self.availability_matrix[self.instr_col] = self.df[self.instr_col]
    for personID in list(self.availability_matrix.index):
      for column in self.times_list:
        if self.df.loc[personID, column] == self.available_keyword:
          self.availability_matrix.loc[personID, column] = 1
        else:
          self.availability_matrix.loc[personID, column] = 0


# Same as before -- make sure this is built before constructng scheduling model object
  def build_instrumentation_matrix(self):
    instrumentation_columns = self.instrument_list
    self.instrumentation_matrix = pd.DataFrame(index=np.arange(len(self.df[self.name_col])),columns=instrumentation_columns)
    for person_ID in list(self.instrumentation_matrix.index):
      for instrument in self.instrument_list:
        if self.df.loc[person_ID,self.instr_col] == instrument:
          self.instrumentation_matrix.loc[person_ID, instrument] = 1
        else:
          self.instrumentation_matrix.loc[person_ID, instrument] = 0

# Same as before yet again -- make sure instrument groups are assigned and somehow check the user.
  def edit_inst_groups(self):
    while True:
      print_list(['Add Instrument Group', 'Remove Instrument Group', 'Reassign Instrument Group', 'Cancel'], 'choices')
      choicenum = integer_choice('Select the number corresponding to the option you would like.',1,4)
      if choicenum == 1:
        self.instrument_groups[str(input('Enter the name of the slot group you would like to create:'))] = []
      elif choicenum == 2:
        print_list(list(self.instrument_groups.keys()), 'slot groups')
        groupnum = integer_choice('Enter the number corresponding to the instrument group you wish to delete.',1,len(self.instrument_groups))
        groupchoice = list(self.instrument_groups.keys())[groupnum-1]
        del self.instrument_groups[groupchoice]
      elif choicenum == 3:
        self.reassign_instruments()
      else:
        return

  def reassign_instruments(self):
    self.instrument_list
    print_list(list(self.instrument_groups.keys()),'instrument group')
    groupnum = integer_choice('Enter the number which corresponds to the slot group you wish you edit.',1,len(self.instrument_groups))
    groupchoice = list(self.instrument_groups.keys())[groupnum-1]
    self.instrument_groups[groupchoice] = []
    print_list(self.instrument_list,'instrument')
    instrnums = integer_choice(f"Enter the number of an instrument you wish to assign to {groupchoice}: \n",1,len(self.instrument_list),True)
    for num in instrnums:
      instrchoice = self.instrument_list[num-1]
      self.instrument_groups[groupchoice].append(instrchoice)
    print(f'The following have been assigned to {groupchoice}:')
    for instrument in self.instrument_groups[groupchoice]:
      print(instrument)

# These functions were made initially just for like debugging and testing sakes, but maybe they will be useful in the future.
  def availability_to_csv(self):
    self.availability_matrix.to_csv('AVAILABILITY.csv',index=True)

  def instrumentation_to_csv(self):
    self.instrumentation_matrix.to_csv('INSTRUMENTATION.csv',index=True)


  def validate_st(self):
    # 1. Slot groups
    if not isinstance(self.slot_groups, dict):
        raise ValueError("Time slot groups are not defined.")
    empty = [k for k,v in self.slot_groups.items() if len(v)==0]
    if empty:
        raise ValueError(f"Time slot groups {empty} are empty (no slots).")

    # 2. Instrument groups
    if not isinstance(self.instrument_groups, dict):
        raise ValueError("Instrument groups are not defined.")
    empty = [k for k,v in self.instrument_groups.items() if len(v)==0]
    if empty:
        raise ValueError(f"Instrument groups {empty} have no instruments.")

    # 3. Instrumentation matrix
    if self.instrumentation_matrix is None:
        raise ValueError("Instrumentation matrix has not been built.")
    if self.instrumentation_matrix.empty:
        raise ValueError("Instrumentation matrix is empty.")

    # 4. Availability matrix
    if self.availability_matrix is None:
        raise ValueError("Availability matrix has not been built.")
    if self.availability_matrix.empty:
        raise ValueError("Availability matrix is empty.")

  def validate_extra(self):
    # 1. Slot groups
    empty1 = [k for k,v in self.slot_groups.items() if len(v)==0]
    empty2 = [k for k,v in self.instrument_groups.items() if len(v)==0]
    if not isinstance(self.slot_groups, dict):
        return("Time slot groups are not defined.")
    
    elif empty1:
        return(f"Time slot groups {empty1} are empty (no slots).")

    # 2. Instrument groups
    elif not isinstance(self.instrument_groups, dict):
        return("Instrument groups are not defined.")
    elif empty2:
        return(f"Instrument groups {empty2} have no instruments.")
    # 3. Instrumentation matrix
    elif self.instrumentation_matrix is None:
        return("Instrumentation matrix has not been built.")
    elif self.instrumentation_matrix.empty:
        return("Instrumentation matrix is empty.")
    # 4. Availability matrix
    elif self.availability_matrix is None:
        return("Availability matrix has not been built.")
    elif self.availability_matrix.empty:
        return("Availability matrix is empty.")
    else:
        return("Success")
