from helpers import integer_choice, print_list
import streamlit as st

def user_instrumentation_constraint(model,combos_list: list,instrument_groups_list: list,instruments_list: list):
    instrumentchoices = instrument_groups_list + instruments_list
    combochoices = combos_list + ['All Combos']
    print_list(combochoices)
    wordedconstraint = ''
    listitem = integer_choice('Select the option corresponding to which combo you would like to assign the constraint to: \n', 1, len(combochoices)) - 1
    chosencombo = combochoices[listitem]
    countlist = ['At Least', 'At Most', 'Exactly']
    print_list(countlist)
    wordedconstraint += f'{chosencombo} must include '
    countitem = integer_choice(f'Fill in the blank: {wordedconstraint} ___: \n',1,3) - 1
    chosencount = countlist[countitem]
    wordedconstraint += f'{chosencount.lower()} '
    userint = integer_choice(f'{wordedconstraint} __: \n',0,10)
    print_list(instrumentchoices)
    wordedconstraint += f'{userint} '
    instrumentitem = integer_choice(f'Fill in the blank: {wordedconstraint}',1,len(instrumentchoices)) - 1
    choseninstrument = instrumentchoices[instrumentitem]
    wordedconstraint += f'of instrument type {choseninstrument}.'
    print(f'Your constraint is: {wordedconstraint}')
    if chosencount.lower() == 'at least':
      bound = 'LB'
    elif chosencount.lower() == 'at most':
      bound = 'UB'
    elif chosencount.lower() == 'exactly':
      bound = 'amt'
    instrumentation_constraint = {
      'combo': chosencombo,
      'type': bound,
      'value': userint,
      'instrument': choseninstrument,
      'inwords': wordedconstraint
    }
    return instrumentation_constraint  
    
"""
# combolist = list(m.Combos.data())
    # instrument_groupslist = self.instrgroupsets
    # instruments_list = list(m.Instruments.data())
    # instrumentchoices = instrument_groupslist + instruments_list

    # # Get info from user
    # combochoices = combolist + ['All Combos']
    # print_list(combochoices)
    # wordedconstraint = ''
    # listitem = integer_choice('Select the option corresponding to which combo you would like to assign the constraint to: \n', 1, len(combochoices)) - 1
    # chosencombo = combochoices[listitem]
    # countlist = ['At Least', 'At Most', 'Exactly']
    # print_list(countlist)
    # wordedconstraint += f'{chosencombo} must include '
    # countitem = integer_choice(f'Fill in the blank: {wordedconstraint} ___: \n',1,3) - 1
    # chosencount = countlist[countitem]
    # wordedconstraint += f'{chosencount.lower()} '
    # userint = integer_choice(f'{wordedconstraint} __: \n',0,10)
    # print_list(instrumentchoices)
    # wordedconstraint += f'{userint} '
    # instrumentitem = integer_choice(f'Fill in the blank: {wordedconstraint}',1,len(instrumentchoices)) - 1
    # choseninstrument = instrumentchoices[instrumentitem]
    # wordedconstraint += f'of instrument type {choseninstrument}.'
    # print(f'Your constraint is: {wordedconstraint}')
    # if chosencount.lower() == 'at least':
    #   bound = 'LB'
    # elif chosencount.lower() == 'at most':
    #   bound = 'UB'
    # elif chosencount.lower() == 'exactly':
    #   bound = 'amt'

    # instrumentation_constraint = {
    #   'combo': chosencombo,
    #   'type': bound,
    #   'value': userint,
    #   'instrument': choseninstrument,
    #   'inwords': wordedconstraint
    # }
"""
    
def user_rehearsal_constraint(model,combos_list: list,slot_groups_list: list):
  wordedconstraint = ''
  combochoices = combos_list + ['All Combos']
  print_list(combochoices)
  listitem = integer_choice('Select the option corresponding to which combo you would like to assign the constraint to: \n', 1, len(combochoices)) - 1
  chosencombo = combochoices[listitem]
  wordedconstraint += f'{chosencombo} must rehearse '
  print_list(slot_groups_list)
  slotsitem = integer_choice(f'{wordedconstraint} in what kind of slot group? \n',1,len(slot_groups_list)) - 1
  chosenslotgroup = slot_groups_list[slotsitem]
  wordedconstraint += f'in slot type {chosenslotgroup.lower()} '
  userint = integer_choice(f'{wordedconstraint} how many times weekly?: \n',0,10)
  wordedconstraint += f'{userint} time weekly.' if userint == 1 else f'{userint} times weekly.'
  print(f'Your constraint is: {wordedconstraint}')

  rehearsal_constraint = {
    'combo': chosencombo,
    'value': userint,
    'slotgroup': chosenslotgroup,
    'inwords': wordedconstraint
  }
  return rehearsal_constraint

""" # Get info from user
    # combochoices = combolist + ['All Combos']
    # print_list(combochoices)
    # wordedconstraint = ''
    # listitem = integer_choice('Select the option corresponding to which combo you would like to assign the constraint to: \n', 1, len(combochoices)) - 1
    # chosencombo = combochoices[listitem]
    # wordedconstraint += f'{chosencombo} must rehearse '
    # print_list(slotgroupslist)
    # slotsitem = integer_choice(f'{wordedconstraint} in what kind of slot group? \n',1,len(slotgroupslist)) - 1
    # chosenslotgroup = slotgroupslist[slotsitem]
    # wordedconstraint += f'in slot type {chosenslotgroup.lower()} '
    # userint = integer_choice(f'{wordedconstraint} how many times weekly?: \n',0,10)
    # wordedconstraint += f'{userint} time weekly.' if userint == 1 else f'{userint} times weekly.'
    # print(f'Your constraint is: {wordedconstraint}')

    # rehearsal_constraint = {
    #   'combo': chosencombo,
    #   'value': userint,
    #   'slotgroup': chosenslotgroup,
    #   'inwords': wordedconstraint
    # } """

def user_combo_size_constraint(model, combos_list):
    combochoices = combos_list + ['All Combos']
    print_list(combochoices)
    wordedconstraint = ''
    listitem = integer_choice('Select the option corresponding to which combo you would like to assign the constraint to: \n', 1, len(combochoices)) - 1
    chosencombo = combochoices[listitem]
    countlist = ['At Least', 'At Most', 'Exactly']
    print_list(countlist)
    wordedconstraint += f'{chosencombo} must have '
    countitem = integer_choice(f'Fill in the blank: {wordedconstraint} ___: \n',1,3) - 1
    chosencount = countlist[countitem]
    wordedconstraint += f'{chosencount.lower()} '
    userint = integer_choice(f'{wordedconstraint} __ people: \n',0,50)

    wordedconstraint += f'{userint} people.'
    print(f'Your constraint is: {wordedconstraint}')

    if chosencount.lower() == 'at least':
      bound = 'LB'
    elif chosencount.lower() == 'at most':
      bound = 'UB'
    elif chosencount.lower() == 'exactly':
      bound = 'amt'

    combo_size_constraint = {
      'combo': chosencombo,
      'type': bound,
      'value': userint,
      'inwords': wordedconstraint
    }

    return combo_size_constraint

"""     # combochoices = combolist + ['All Combos']
    # print_list(combochoices)
    # wordedconstraint = ''
    # listitem = integer_choice('Select the option corresponding to which combo you would like to assign the constraint to: \n', 1, len(combochoices)) - 1
    # chosencombo = combochoices[listitem]
    # countlist = ['At Least', 'At Most', 'Exactly']
    # print_list(countlist)
    # wordedconstraint += f'{chosencombo} must have '
    # countitem = integer_choice(f'Fill in the blank: {wordedconstraint} ___: \n',1,3) - 1
    # chosencount = countlist[countitem]
    # wordedconstraint += f'{chosencount.lower()} '
    # userint = integer_choice(f'{wordedconstraint} __ people: \n',0,50)

    # wordedconstraint += f'{userint} people.'
    # print(f'Your constraint is: {wordedconstraint}')

    # if chosencount.lower() == 'at least':
    #   bound = 'LB'
    # elif chosencount.lower() == 'at most':
    #   bound = 'UB'
    # elif chosencount.lower() == 'exactly':
    #   bound = 'amt'

    # combo_size_constraint = {
    #   'combo': chosencombo,
    #   'type': bound,
    #   'value': userint,
    #   'inwords': wordedconstraint
    # } """

def remove_old_constraints(object,model,constraint_type):
  md = model

  allowedtypes = ['instrumentation','rehearsal','combo_size']
  if constraint_type not in allowedtypes:
    raise ValueError(f"mode must be one of {allowedtypes}, got '{constraint_type}'.")
  
  if constraint_type == 'instrumentation':
    for oldconstraint in object.implementedinstrconstraints:
      combo = oldconstraint['combo']
      bound = oldconstraint['type']
      instrument = oldconstraint['instrument']
      if combo != 'All Combos':
        comboname = f"{combo.replace(' ','_').lower()}_"
      else:
        comboname = ''
      constraint_name = comboname + instrument.lower() + '_' + bound

      if hasattr(md,constraint_name):
        md.del_component(getattr(md, constraint_name))
      if constraint_name in object.implementedconstraints:
        del object.implementedconstraints[constraint_name]
        print(f"Removed constraint {constraint_name}")

    object.implementedinstrconstraints = []


    '''
        for oldconstraint in self.implementedinstrconstraints:
      combo = oldconstraint['combo']
      bound = oldconstraint['type']
      instrument = oldconstraint['instrument']
      if combo != 'All Combos':
        comboname = f"{combo.replace(' ','_').lower()}_"
      else:
        comboname = ''
      constraint_name = comboname + instrument.lower() + '_' + bound

      if hasattr(m,constraint_name):
        m.del_component(getattr(m, constraint_name))
      if constraint_name in self.implementedconstraints:
        del self.implementedconstraints[constraint_name]
        print(f"Removed constraint {constraint_name}")

    self.implementedinstrconstraints = []
    '''


  elif constraint_type == 'rehearsal':
    for oldconstraint in object.implementedinstrconstraints:
      combo = oldconstraint['combo']
      bound = oldconstraint['type']

      if combo != 'All Combos':
        comboname = f"{combo.replace(' ','_').lower()}_"
      else:
        comboname = 'allcombos'
      constraint_name = comboname + '_size_' + bound

      if hasattr(md,constraint_name):
        md.del_component(getattr(md, constraint_name))
        print(f"Removed constraint {constraint_name}")
      if constraint_name in object.implementedconstraints:
        del object.implementedconstraints[constraint_name]

      '''
    for oldconstraint in self.implementedrehearsalconstraints:
      combo = oldconstraint['combo']
      slotgroup = oldconstraint['slotgroup']
  
      groupsetname = self.slotgroupsdict[slotgroup]

      if combo != 'All Combos':
        comboname = f"{combo.replace(' ','_').lower()}_"
      else:
        comboname = ''
      constraint_name = comboname + groupsetname

      if hasattr(m,constraint_name):
        m.del_component(getattr(m, constraint_name))
      if constraint_name in self.implementedconstraints:
        del self.implementedconstraints[constraint_name]
        print(f"Removed constraint {constraint_name}")

    self.implementedrehearsalconstraints = []
      '''

    object.implementedrehearsalconstraints = []


  elif constraint_type == 'combo_size':
    for oldconstraint in object.implementedinstrconstraints:
      combo = oldconstraint['combo']
      bound = oldconstraint['type']

      if combo != 'All Combos':
        comboname = f"{combo.replace(' ','_').lower()}_"
      else:
        comboname = 'allcombos'
      constraint_name = comboname + '_size_' + bound

      if hasattr(md,constraint_name):
        md.del_component(getattr(md, constraint_name))
        print(f"Removed constraint {constraint_name}")
      if constraint_name in object.implementedconstraints:
        del object.implementedconstraints[constraint_name]

    object.implementedsizeconstraints = []

    
'''
    for oldconstraint in self.implementedinstrconstraints:
      combo = oldconstraint['combo']
      bound = oldconstraint['type']

      if combo != 'All Combos':
        comboname = f"{combo.replace(' ','_').lower()}_"
      else:
        comboname = 'allcombos'
      constraint_name = comboname + '_size_' + bound

      if hasattr(m,constraint_name):
        m.del_component(getattr(m, constraint_name))
        print(f"Removed constraint {constraint_name}")
      if constraint_name in self.implementedconstraints:
        del self.implementedconstraints[constraint_name]

    self.implementedsizeconstraints = []
    '''


def remove_old_constraints_st(object,constraint_type):
  md = object.model

  allowedtypes = ['instrumentation','rehearsal','combo_size']
  if constraint_type not in allowedtypes:
    raise ValueError(f"mode must be one of {allowedtypes}, got '{constraint_type}'.")
  
  if constraint_type == 'instrumentation':
    for oldconstraint in object.implementedinstrconstraints:
      combo = oldconstraint['combo']
      bound = oldconstraint['type']
      instrument = oldconstraint['instrument']
      if combo != 'All Combos':
        comboname = f"{combo.replace(' ','_').lower()}_"
      else:
        comboname = ''
      constraint_name = comboname + instrument.lower() + '_' + bound

      if hasattr(md,constraint_name):
        md.del_component(getattr(md, constraint_name))
      if constraint_name in object.implementedconstraints:
        del object.implementedconstraints[constraint_name]
        # st.success(f"Removed constraint {constraint_name}")

    object.implementedinstrconstraints = []

  elif constraint_type == 'rehearsal':
    for oldconstraint in object.implementedinstrconstraints:
      combo = oldconstraint['combo']
      bound = oldconstraint['type']

      if combo != 'All Combos':
        comboname = f"{combo.replace(' ','_').lower()}_"
      else:
        comboname = 'allcombos'
      constraint_name = comboname + '_size_' + bound

      if hasattr(md,constraint_name):
        md.del_component(getattr(md, constraint_name))
        # st.success(f"Removed constraint {constraint_name}")
      if constraint_name in object.implementedconstraints:
        del object.implementedconstraints[constraint_name]

    object.implementedrehearsalconstraints = []


  elif constraint_type == 'combo_size':
    for oldconstraint in object.implementedinstrconstraints:
      combo = oldconstraint['combo']
      bound = oldconstraint['type']

      if combo != 'All Combos':
        comboname = f"{combo.replace(' ','_').lower()}_"
      else:
        comboname = 'allcombos'
      constraint_name = comboname + '_size_' + bound

      if hasattr(md,constraint_name):
        md.del_component(getattr(md, constraint_name))
        # st.success(f"Removed constraint {constraint_name}")
      if constraint_name in object.implementedconstraints:
        del object.implementedconstraints[constraint_name]

    object.implementedsizeconstraints = []
