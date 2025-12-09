# This class handles the building of the model -- ie the stressful part that hopefully does not burn to the ground when I try to run it.
import numpy as np
import pandas as pd
from pyomo.environ import *
import pyomo.environ as pyo
from pyomo.opt import SolverFactory

from helpers import print_list, integer_choice, safe_run
from responsereader import ResponseData
import constraintmanager as cm
import streamlit as st

print("Loading model_builder")

# Set Solver
solver = SolverFactory('cbc')

class SchedulingModel:
  def __init__(self, data: ResponseData):
    data.validate_st()
    self.data = data # data is the response data object -- hopefully will tell the scheduling model how to read the csv (if everything that needs to be defined has been)
    self.model = pyo.ConcreteModel() # creates the model
    self.slotgroupsets = [] # this list will hold the names of the slot groups after they've been transformed to be pyomo-compatible
    self.instrgroupsets = [] # similar pyomo-cmpatability list, but for instrument groups
    self.instrumentationconstraints = [] # will hold dictionaries containing key information for instrumentation constraints -- enough to build the constraint off of
    self.implementedinstrconstraints = [] # will hold the dictionaries that correspond to instrumentation constraints that have already been implemented into the model
    self.rehearsalconstraints = [] # will hold dictionaries containing key info on rehearsal constraints
    self.implementedrehearsalconstraints = [] # will hold the dictionaries corresponding to rehearsal constraints that have been implemented into the model
    self.combosizeconstraints = [] # again, holds combo size dictionaries
    self.implementedsizeconstraints = [] # again, holds combo size dictionaries that have been implemented.
    self.slotgroupsdict = {} # converts between slotgroup names and the pyomo compatible slotgroupset names
    self.toggleableconstraints = { # initializes all toggleable constraints as ON.
        'no_instr_repeats': True,
        'one_combo_max': True,
        'no_slot_repeats': True,
        'slot_availability': True
        # TO DO: MOVE AVAILABILITY CONSTRAINT HERE SO THAT ALL 'non-customizable' CONSTRAINTS ARE IMPLEMENTED AT THE SAME TIME
    }
    self.implementedconstraints = {} # list of all constraints that have been implemented.
    self.thingsbuilt = False # is false until the model has been initialized.

  # kickstart_model makes sure all the things are defined BEFORE building constraints and whatnot off of them.
  def kickstart_model_st(self):
    self.create_sets_st()
    self.create_variables()
    self.create_parameters()
    self.create_objective() # TO DO: IMPLEMENT CONSTRAINT SYSTEM THAT a) MAXIMIZES PREFERENCE AND b) MAXIMIZES # REAL PPL SCHEDULED
    self.thingsbuilt = True
    print('Hooray!')    

  def replace_constraint(self, model, name, new_constraint):
    if hasattr(model, name):
        model.del_component(getattr(model, name))
    setattr(model, name, new_constraint)

  def solve_model(self):
    if hasattr(self, "comboAssignments"):
      del self.comboAssignments
    m = self.model
    # m.pprint()
    result = solver.solve(m)

    if result.solver.termination_condition != pyo.TerminationCondition.optimal:
      st.warning("Model is infeasible or did not solve to optimality.")
      solvedgood = False
    else:
      solvedgood = True
    st.write('Solver Status:', result.solver.status)
    st.write('Termination Condition:', result.solver.termination_condition)

    # Build matrix with name, instrument, bin combo assignment:
    self.comboAssignments = pd.DataFrame(index=list(np.arange(len(self.data.df[self.data.name_col]))),columns=['Name','Instrument'] + self.comboslist)
    for personID in self.comboAssignments.index:
      self.comboAssignments.loc[personID,'Name'] = self.data.names_list[personID]
      self.comboAssignments.loc[personID,'Instrument'] = self.data.df.loc[personID,self.data.instr_col]
      for combo in self.comboslist:
        self.comboAssignments.loc[personID,combo] = int(pyo.value(m.x[personID,combo]))
    self.comboAssignments.to_csv('TESTSOLVED',index=True) # For debugging and testing purposes, remove later.
    return solvedgood
  
  def get_rehearsal_assignments(self):
      m = self.model
      
      rehearsal_rows = []

      for groupset in self.slotgroupsets:
          varname = 'y_' + groupset
          slots = getattr(m, groupset)      # the slot names
          y = getattr(m, varname)           # the Pyomo variable

          for c in m.Combos:
              for s in slots:
                  if int(pyo.value(y[c, s])) == 1:
                      rehearsal_rows.append({
                          "Combo": str(c),
                          "Slot Group": groupset,
                          "Slot": str(s)
                      })

      radf = pd.DataFrame(rehearsal_rows)
      return radf
      # radf.to_csv("rehearsal_assignments.csv", index=True)

  def get_combo_assignments(self):

    if not hasattr(self, "comboAssignments"):
      st.warning("Error: Model has not been solved successfully. No assignments available.")
      return {}
        
    combo_dict = {}
    ca_df = self.comboAssignments
    try:
      combocolumns = [col for col in ca_df.columns if col not in ['Name','Instrument']]
      for combo in combocolumns:
        combodf = ca_df.loc[ca_df[combo]==1, ['Name','Instrument']]
        # setattr(self,f'{combo}_assignments',ca_df[['Name','Instrument']][ca_df[combo]==1])
        # combodf = getattr(self,f'{combo}_assignments')
        # combodf.to_csv(f'{combo}_assignment.csv',index=True) 
        combo_dict[combo] = combodf
      return combo_dict
      
    except Exception as e:
      st.warning(f'An error has occured: {e}. Try again.') #ood

  def create_sets_st(self):
    m = self.model
    m.Person = pyo.Set(initialize=[int(i) for i in range(len(self.data.names_list))])
    m.Instruments = pyo.Set(initialize=self.data.instrument_list)
    # Create Slot Group sets
    for slot_group, slots in self.data.slot_groups.items():
      setname = slot_group.replace(" ","_")
      setattr(m, setname, pyo.Set(initialize=slots,ordered=True))
      self.slotgroupsets.append(setname)
      self.slotgroupsdict[slot_group] = setname
    # Create Instrument Group sets
    for instrument_group, instruments in self.data.instrument_groups.items():
      setname = instrument_group.replace(" ","_")
      setattr(m, setname, pyo.Set(initialize=instruments,ordered=True))
      self.instrgroupsets.append(setname)
    # Create Combos set


    # comboscount = integer_choice('How many combos would you like to schedule? \n',1,50)
    # for i in range(comboscount):
    #   comboname = str(input(f"What is the name of Combo {i+1}?"))
    #   if comboname in self.comboslist:
    #     comboname = str(input(f"That combo already exists! Please select a new name for Combo {i+1}."))
    #   self.comboslist.append(comboname)

    m.Combos = pyo.Set(initialize=self.comboslist)

  def create_variables(self):
    m = self.model
    m.x = pyo.Var(m.Person,m.Combos,domain=pyo.Binary) #x_nc = 1 if student n assigned to combo j, 0 otherwise
    for groupset in self.slotgroupsets:
      varname = 'y_' + groupset
      setattr(m, varname, pyo.Var(m.Combos,getattr(m,groupset),domain=pyo.Binary))

  def create_parameters(self):
    m = self.model
    instrumentation_dict_a = self.data.instrumentation_matrix.stack().to_dict()
    instrumentation_dict_b = {
        (int(p),str(ci)): val
        for (p,ci), val in instrumentation_dict_a.items()
    }

    m.Plays = pyo.Param(m.Person,m.Instruments,initialize=instrumentation_dict_b,within=pyo.Binary,default=0) #for some reason default=0 keeps the code from breaking
    for groupset in self.slotgroupsets:
      avail_dict = self.data.availability_matrix[list(getattr(m,groupset).data())].stack().to_dict()
      slots = getattr(m,groupset)
      paramname = 'av_' + groupset
      setattr(m, paramname, pyo.Param(m.Person,slots,initialize=avail_dict,within=pyo.Binary))

  def create_objective(self):
    m = self.model
    total_assigned = sum(m.x[p,c] for p in m.Person for c in m.Combos)
    big_M = 1000
    m.Obj = Objective(expr=big_M*total_assigned,sense=maximize) # add preference later

  def build_instrumentation_constraints(self):
    m = self.model
    instrument_groupslist = self.instrgroupsets

    for constraint in self.instrumentationconstraints:
      combo = constraint['combo']
      bound = constraint['type']
      value = constraint['value']
      instrument = constraint['instrument']
      inwords = constraint['inwords']

      if combo != 'All Combos':
        comboname = f"{combo.replace(' ','_').lower()}_"
      else:
        comboname = ''
      constraint_name = comboname + instrument.lower() + '_' + bound

      if instrument in instrument_groupslist:
        checkedinstrs = getattr(m, instrument)
      else:
        checkedinstrs = [str(instrument)]
      combo_set = [combo] if combo != 'All Combos' else m.Combos
      # val=instrumentation_constraint['value']

      def rule(m,c,checkedinstrs=checkedinstrs, val=value):
        expr = sum(sum(m.x[p,c]*m.Plays[p,ci] for p in m.Person) for ci in checkedinstrs)
        if bound == 'LB':
          return expr >= val
        elif bound == 'UB':
          return expr <= val
        else:
          return expr == val

      self.replace_constraint(m, constraint_name, pyo.Constraint(combo_set, rule=rule))
      st.success(f'Added constraint: {constraint_name} as {inwords}')
      self.implementedinstrconstraints.append(constraint)
      self.implementedconstraints[constraint_name] = inwords

  def build_rehearsal_constraints(self):
    m = self.model
    slotgroupslist = list(self.slotgroupsdict.keys())

    # cm.remove_old_constraints(self,m,'rehearsal')

    for constraint in self.rehearsalconstraints:
      combo = constraint['combo']
      value = constraint['value']
      slotgroup = constraint['slotgroup']
      inwords = constraint['inwords']

      groupsetname = self.slotgroupsdict[slotgroup]

      if combo != 'All Combos':
        comboname = f"{combo.replace(' ','_').lower()}_"
      else:
        comboname = 'allcombos'
      constraint_name = comboname + groupsetname

      if slotgroup in slotgroupslist:
        checkedslots = getattr(m, groupsetname)
      else:
        st.error('An error has occured. This message should not be displayed. Returning Function.')
        return

      combo_set = [combo] if combo != 'All Combos' else m.Combos

      # val=instrumentation_constraint['value']

      varname = 'y_' + groupsetname
      def rule(m,c,checkedslots=checkedslots, val=value):
        expr = sum(getattr(m,varname)[c,slot] for slot in checkedslots)
        return expr == val

      self.replace_constraint(m, constraint_name, pyo.Constraint(combo_set, rule=rule))
      st.success(f'Added constraint: {constraint_name} as {inwords}')
      self.implementedrehearsalconstraints.append(constraint)
      self.implementedconstraints[constraint_name] = inwords

  def build_combo_size_constraints(self):
    m = self.model

    for constraint in self.combosizeconstraints:
      combo = constraint['combo']
      bound = constraint['type']
      value = constraint['value']
      inwords = constraint['inwords']

      if combo != 'All Combos':
        comboname = f"{combo.replace(' ','_').lower()}_"
      else:
        comboname = 'allcombos'
      constraint_name = comboname + '_size_' + bound

      combo_set = [combo] if combo != 'All Combos' else m.Combos

      def rule(m,c, val=value):
        expr = sum(m.x[p,c] for p in m.Person)
        if bound == 'LB':
          return expr >= val
        elif bound == 'UB':
          return expr <= val
        else:
          return expr == val

      self.replace_constraint(m, constraint_name, pyo.Constraint(combo_set, rule=rule))
      st.success(f'Added constraint: {constraint_name} as {inwords}')
      self.implementedsizeconstraints.append(constraint)
      self.implementedconstraints[constraint_name] = inwords

  def build_toggle_constraints(self):
    m = self.model

    # no_instr_repeats = each combo has at most 1 of a given instrument
    if self.toggleableconstraints['no_instr_repeats']:
      def rule(m,c,i):
        expr = sum(m.x[p,c]*m.Plays[p,i] for p in m.Person)
        return expr <= 1
      self.replace_constraint(m,'no_instr_repeats',pyo.Constraint(m.Combos,m.Instruments,rule=rule))
      st.success(f'Added constraint: "no_instr_repeats" as "Each combo may not have more than 1 of a given instrument".')
      self.implementedconstraints['no_instr_repeats'] = "Each combo may not have more than 1 of a given instrument"
    else:
      if hasattr(m, 'no_instr_repeats'):
          m.del_component('no_instr_repeats')
          del(self.implementedconstraints['no_instr_repeats'])
          st.warning(f'Removed constraint: "no_instr_repeats"')

    # one_combo_max = each individual assigned to at most 1 combo
    if self.toggleableconstraints['one_combo_max']:
      def rule(m,p):
        expr = sum(m.x[p,c] for c in m.Combos)
        return expr <= 1
      self.replace_constraint(m,'one_combo_max',pyo.Constraint(m.Person,rule=rule))
      st.success('Added constraint: "one_combo_max" as "Each person may be assigned to at most 1 combo".')
      self.implementedconstraints['one_combo_max'] = "Each person may be assigned to at most 1 combo"
    else:
      if hasattr(m, 'one_combo_max'):
          m.del_component('one_combo_max')
          del(self.implementedconstraints['one_combo_max'])
          st.warning(f'Removed constraint: "one_combo_max"')

    # no_slot_repeats = each slot is only used once
    slotgroupslist = list(self.slotgroupsdict.keys())

    if self.toggleableconstraints['no_slot_repeats']:
      for slotgroup in slotgroupslist:
        groupsetname = self.slotgroupsdict[slotgroup]
        slots = getattr(m,groupsetname)
        varname = 'y_' + groupsetname
        slot_var = getattr(m,varname)
        constraint_name = groupsetname + '_usage'
        def rule(m,s, slot_var = slot_var):
          expr = sum(slot_var[c,s] for c in m.Combos)
          return expr <= 1
        self.replace_constraint(m,constraint_name,pyo.Constraint(slots,rule=rule))
        st.success(f'Added constraint: {constraint_name} as "Each slot in {slotgroup} may be assigned to at most 1 combo."')
        self.implementedconstraints[constraint_name] = f"Each slot in {slotgroup} may be assigned to at most 1 combo."
    else:
        for slotgroup in slotgroupslist:
          groupsetname = self.slotgroupsdict[slotgroup]
          constraint_name = groupsetname + '_usage'
          if hasattr(m, constraint_name):
            m.del_component(getattr(m,constraint_name))
            del(self.implementedconstraints[constraint_name])
            st.warning(f'Removed constraint: {constraint_name}')

    # slot_availability = each person must be available for the slot their combo is assigned
    for slotgroup in slotgroupslist:
      groupsetname = self.slotgroupsdict[slotgroup]
      checkedslots = getattr(m, groupsetname)
      constraint_name = groupsetname + '_avail'
      param_name = 'av_' + groupsetname
      var_name = 'y_' + groupsetname
      avail_param = getattr(m,param_name)
      rehearsal_var = getattr(m, var_name)
      def rule(m,p,c,checkedslots=checkedslots):
        expr = m.x[p,c] - sum(avail_param[p,slot]*rehearsal_var[c,slot] for slot in checkedslots)
        return expr <= 0
      if self.toggleableconstraints['slot_availability']:
        self.replace_constraint(m, constraint_name, pyo.Constraint(m.Person, m.Combos, rule=rule))
        inwords = f'Each person must be available for their assigned {slotgroup} rehearsal(s).'
        st.success(f'Added constraint: {constraint_name} as {inwords}')
        self.implementedconstraints[constraint_name] = inwords
      else:
          if hasattr(m, constraint_name):
            m.del_component(getattr(m,constraint_name))
            del(self.implementedconstraints[constraint_name])
            st.warning(f'Removed constraint: {constraint_name}')

    return

  def debug(self):
    m = self.model
    for p in m.Person:
      for c in m.Combos:
        print(type(m.x[p,c]))
    for p in m.Person:
      for ci in m.Instruments:
        print(type(m.Plays[p,ci]))



