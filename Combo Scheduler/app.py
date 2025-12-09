import streamlit as st
import pandas as pd

from responsereader import ResponseData
from modelbuilder import SchedulingModel
from constraintmanager import remove_old_constraints_st

# tab_home, tab_load, tab_csvnames, tab_instr, tab_slotgroups, tab_instrgroups, tab_matrices = st.tabs([
#     "Home",
#     "Load Data",
#     "CSV Settings",
#     "Instruments",
#     "Rehearsal Time Groups",
#     "Instrument Type Groups",
#     "Prepare Data"
# ])
if "ready_for_assignments" not in st.session_state:
    st.session_state.ready_for_assignments = 'notready'

if "tab_state" not in st.session_state:
    st.session_state.tab_state = 'Empty'

if "confirm_schedule_box" not in st.session_state:
    st.session_state.confirm_schedule_box = False
    
if "confirm_reset_constraints" not in st.session_state:
    st.session_state.confirm_reset_constraints = False

if "confirm_combo_reset" not in st.session_state:
    st.session_state.confirm_combo_reset = False

if "kickstarted" not in st.session_state:
    st.session_state.kickstarted = False

state = st.session_state.tab_state

#if state == 'Empty' or state == 'ResponseData':
tab_home, tab_load = st.tabs([
    "Home",
    "Load Data"
])



with tab_home:
    st.title('Jazz Combo Scheduler')
    st.write('By Jake Lee :)')

    if st.button('Restart Program'):
        st.session_state.restart_program = True

    if "restart_program" in st.session_state:
        st.warning('Are you sure? This will delete all progress made so far.')
        col1, col2, col3 = st.columns([1,1,7])
        if col1.button('Yes',key='confirmrestartyes'):
            st.session_state.confirm_restart = True
            del st.session_state.restart_program
            st.rerun()
        if col2.button('No',key='confirmrestartno'):
            del st.session_state.restart_program
            st.rerun()
    
    if "confirm_restart" in st.session_state:
        st.session_state.clear()
        st.rerun()

with tab_load:
    uploaded = st.file_uploader("Upload your response CSV", type=["csv"])

    if "rd_initialized" not in st.session_state:
        st.session_state.rd_initialized = False

    if uploaded:
        df = pd.read_csv(uploaded)
        st.success("CSV Loaded!")
        st.write("Preview of uploaded data:")
        st.dataframe(df)

        if 'responsedata' not in st.session_state:
            mydata = ResponseData(df)
            st.success('Survey loaded into ResponseData Class')
            st.session_state.responsedata = mydata
            st.session_state.rd_initialized = True
            st.session_state.tab_state = 'ResponseData'
        # else:
            # if "responsedata" in st.session_state:
            #     del st.session_state["responsedata"]
            # if "schedulingmodel" in st.session_state:
            #     del st.session_state["schedulingmodel"]
        #     st.session_state.rd_initialized = False
        #     st.session_state.tab_state = 'ResponseData'
        #     st.rerun()

if st.session_state.tab_state == 'ResponseData':
    tab_csvnames, tab_instr, tab_slotgroups, tab_instrgroups,tab_matrices, tab_createmodel = st.tabs([
        "CSV Settings",
        "Instruments",
        "Rehearsal Time Groups",
        "Instrument Type Groups",
        "Prepare Data",
        "Begin Scheduling"
    ])        
    
    # Name Column
    with tab_csvnames:
        if not st.session_state.rd_initialized:
            st.write('Please upload a file before configuring CSV settings.')
        else:
            st.subheader("Name Column")
            current_namecol = st.session_state.responsedata.name_col
            st.write(f"Current name column: {current_namecol}")

            new_name_col = st.selectbox("Select the column of the CSV file which contains the names of students.",
                                        st.session_state.responsedata.columnslist)

            if st.button("Update Name Column"):
                st.session_state.update_name_column = new_name_col
            
            if "update_name_column" in st.session_state:
                st.session_state.responsedata.name_col = st.session_state.update_name_column
                st.success(f"Name column updated to: {st.session_state.update_name_column}")
                del st.session_state.update_name_column
                st.rerun()


        # Instrument Column
        st.subheader("Instrument Column")
        current_instrcol = st.session_state.responsedata.instr_col
        st.write(f"Current instrument column: {current_instrcol}")

        new_instr_col = st.selectbox("Select the column of the CSV file which contains the students' instruments.",
                                    st.session_state.responsedata.columnslist)

        if st.button("Update Instrument Column"):
            st.session_state.update_instrument_column = new_instr_col

        if "update_instrument_column" in st.session_state:
            st.session_state.responsedata.instr_col = st.session_state.update_instrument_column
            st.success(f"Instrument column updated to: {st.session_state.update_instrument_column}")
            del st.session_state.update_instrument_column
            st.rerun()


        # Availability Keywords
        st.subheader("Availability Keywords")
        current_available_kw = st.session_state.responsedata.available_keyword
        current_unavailable_kw = st.session_state.responsedata.unavailable_keyword
        st.write(f"Current 'Available' Keyword: {current_available_kw}")
        new_avail_kw = st.text_input("Edit 'Available' Keyword? This word is shown in the csv" \
        " file where a student is available at a certain time.",key='availkwbox').strip()

        if st.button("Update 'Available' Keyword"):
            st.session_state.update_available_kw = new_avail_kw

        if "update_available_kw" in st.session_state:
            st.session_state.responsedata.available_keyword = st.session_state.update_available_kw
            st.success(f"'Available' Keyword updated to: {st.session_state.update_available_kw}")
            current_available_kw = st.session_state.responsedata.available_keyword
            del st.session_state.update_available_kw
            st.rerun()


        current_unavailable_kw = st.session_state.responsedata.unavailable_keyword
        st.write(f"Current 'Unavailable' Keyword: {current_unavailable_kw}")
        new_unavail_kw = st.text_input("Edit 'Unavailable' Keyword? This word is shown in the csv" \
        " file where a student is NOT available at a certain time.",key='unavailkwbox').strip()

        if st.button("Update 'Unavailable' Keyword"):
            st.session_state.update_unavailable_kw = new_unavail_kw

        if "update_unavailable_kw" in st.session_state:
            st.session_state.responsedata.unavailable_keyword = st.session_state.update_unavailable_kw
            st.success(f"'Available' Keyword updated to: {st.session_state.update_unavailable_kw}")
            current_unavailable_kw = st.session_state.responsedata.unavailable_keyword
            del st.session_state.update_unavailable_kw
            st.rerun()

        # Instrument List
    with tab_instr:
        if not st.session_state.rd_initialized:
            st.write('Please upload a file before viewing or editing instruments.')
        else:
            st.subheader("Instrument List")
            st.write("The following are the instruments which may appear in the loaded CSV file.")
            inst_list = st.session_state.responsedata.instrument_list
            for inst in inst_list:
                col1, col2 = st.columns([4,1])
                col1.write(inst)
                if col2.button("Delete", key=f"del_{inst}"):
                    inst_list.remove(inst)
                    st.success(f"Removed {inst}")
                    st.rerun()

            new_instrument = st.text_input("Add Instrument? Ensure you enter the instrument exactly as it"
            " will appear in the datasheet.",key='newinstr_tbox').strip()

            if st.button("Add Instrument"):
                if new_instrument and new_instrument not in inst_list:
                    inst_list.append(new_instrument)
                    st.success(f"Added {new_instrument}")
                    st.rerun()
                elif new_instrument in inst_list:
                    st.warning(f"{new_instrument} is already in the Instrument list!")
                elif not new_instrument:
                    st.warning("You did not enter an instrument!")

        # Time Slot Groups
    with tab_slotgroups:
        if not st.session_state.rd_initialized:
            st.write('Please upload a file before viewing or editing instruments.')
        else:    
            st.subheader("Rehearsal Time Groups")
            time_groups = st.session_state.responsedata.slot_groups

            slot_editing = st.session_state.get("editing_slotgroup",None)
            slot_deleting = st.session_state.get("deleting_slotgroup",None)



            col1, col2, col3, col4 = st.columns([4,7,4,4])
            for group, times in time_groups.items():
                col1.write(group)
                col1.write('\n')
                if not times:
                    col2.write("No times assigned yet!")
                    col2.write('\n')
                else:
                    col2.write(", ".join([f"**{slot}**" for slot in times]))
                    # col2.write(times)


                # Edit Button
                if col3.button("Edit Group",key=f"slotedit_{group}"):
                    st.session_state.editing_slotgroup = group
                    st.rerun()
                
                if col4.button('Delete Group',key=f"slotdel_{group}"):
                    st.session_state.deleting_slotgroup = group
                    st.rerun()

                if slot_deleting == group:
                    del time_groups[group]
                    st.session_state.deleting_slotgroup = None
                    st.rerun()

                # Edit slot group
                if slot_editing == group:
                    responseclass = st.session_state.responsedata
                    st.write(f"Editing times in: **{group}**")
                    all_time_slots = [column for column in responseclass.columnslist if column != responseclass.instr_col and column != responseclass.name_col]
                    time_slot_options = []
                    used_time_slots = []
                    for g, s in time_groups.items():
                        if g != group:
                            used_time_slots += s
                    time_slot_options = [i for i in all_time_slots if i not in used_time_slots]

                    selected_slots = st.multiselect(
                        f"Select the rehearsal times that belong to group: {group}",
                        options=time_slot_options,
                        default=times,
                        key=f"slotmultiselect_{group}"
                    )
                
                    if st.button("Save Changes",key=f"slotsave_{group}"):
                        time_groups[group] = selected_slots
                        st.session_state.editing_slotgroup = None
                        st.rerun()

                    if st.button("Cancel",key=f"slotcancel_{group}"):
                        st.session_state.editing_slotgroup = None
                        st.rerun()
            
            if st.button('Add New Rehearsal Type',key='addslotgroup'):
                st.session_state.adding_slotgroup = True

            if "adding_slotgroup" in st.session_state:
                new_group_name = st.text_input('What is the name of the Rehearsal Type').strip()
                if st.button('Save Group'):
                    time_groups[new_group_name] = []
                    del st.session_state.adding_slotgroup
                    st.rerun()
                if st.button('Cancel'):
                    del st.session_state.adding_slotgroup
                    st.rerun()

        # Time Instrument Groups
    with tab_instrgroups:
        if not st.session_state.rd_initialized:
            st.write('Please upload a file before viewing or editing instruments.')
        else:    
            st.subheader("Instrument Type Groups")
            instr_groups = st.session_state.responsedata.instrument_groups

            instr_editing = st.session_state.get("editing_instrgroup",None)
            instr_deleting = st.session_state.get("deleting_instrgroup",None)

            col1, col2, col3, col4 = st.columns([4,7,4,4])
            for group, instruments in instr_groups.items():
                col1.write(group)
                col1.write('\n')
                if not instruments:
                    col2.write("No instruments assigned yet!")
                    col2.write('\n')
                else:
                    col2.write(", ".join([f"**{instrument}**" for instrument in instruments]))


                # Edit Button
                if col3.button("Edit Group",key=f"instredit_{group}"):
                    st.session_state.editing_instrgroup = group
                    st.rerun()

                if col4.button('Delete Group',key=f"instrdel_{group}"):
                    st.session_state.deleting_instrgroup = group
                    st.rerun()

                if instr_deleting == group:
                    del instr_groups[group]
                    st.session_state.deleting_instrgroup = None
                    st.rerun()


                # Edit slot group
                if instr_editing == group:
                    st.write(f"Editing times in: **{group}**")
                    all_instruments = st.session_state.responsedata.instrument_list
                    selected_instruments = st.multiselect(
                        f"Select the instruments that beong to group: {group}",
                        options=all_instruments,
                        default=instruments,
                        key=f"instrmultiselect_{group}"
                    )
                
                    if st.button("Save Changes",key=f"instrsave_{group}"):
                        instr_groups[group] = selected_instruments
                        st.session_state.editing_instrgroup = None
                        st.rerun()

                    if st.button("Cancel",key=f"instrcancel_{group}"):
                        st.session_state.editing_instrgroup = None
                        st.rerun()        
                
            if st.button('Add New Instrument Grouping',key='addinstrgroup'):
                st.session_state.adding_instrgroup = True

            if "adding_instrgroup" in st.session_state:
                new_instr_group_name = st.text_input('What is the name of the Instrument Grouping?').strip()
                if st.button('Save Group',key='saveinstgroup'):
                    instr_groups[new_instr_group_name] = []
                    del st.session_state.adding_instrgroup
                    st.rerun()
                if st.button('Cancel'):
                    del st.session_state.adding_instrgroup
                    st.rerun()



    with tab_matrices:
        # availability
        st.subheader('Availability')
        st.write("*Please review your settings related to availability below:*")
        st.write('---')

        coltext, colkw = st.columns([4,1])
        for text in ['Current "Available" Keyword:','Current "Unavailable" Keyword:']:
            coltext.write(text)
        for kw in [st.session_state.responsedata.available_keyword,st.session_state.responsedata.unavailable_keyword]:
            colkw.write(kw)

        time_groups = st.session_state.responsedata.slot_groups

        col1, col2 = st.columns([1,4])
        for group, times in time_groups.items():
            col1.write(group)
            if not times:
                col2.write("No times assigned yet!")
            else:
                col2.write(f"**{slot}**, "  for slot in times)
        st.write('---')
        st.write('*If the above information appears to your liking, prepare the availability.*')
        if st.button("Prepare Availability"):
            st.session_state.responsedata.build_availability_matrix()
            st.session_state.availmatrixbuilt = True

        if "availmatrixbuilt" not in st.session_state:
            st.session_state.availmatrixbuilt = False

        if st.session_state.availmatrixbuilt:
            if st.button("View Availability Matrix"):
                availmatrix = st.session_state.responsedata.availability_matrix
                st.dataframe(availmatrix)
                if st.button("Hide Availability Matrix"):
                    st.rerun()
        st.write('---')

        # instrumentation
        st.subheader('Instrumentation')
        st.write("*Please review your settings related to instrumentation below:*")
        st.write('---')

        st.write('List of possible instruments in data:')
        st.write(", ".join([f"**{instrument}**" for instrument in st.session_state.responsedata.instrument_list]))
        instr_groups = st.session_state.responsedata.instrument_groups

        i_col1, i_col2 = st.columns([1,4])
        for group, instrs in instr_groups.items():
            i_col1.write(group)
            if not instrs:
                i_col2.write("No instruments assigned yet!")
            else:
                i_col2.write(f"**{inst}**, "  for inst in instrs)
        st.write('---')
        st.write('*If the above information appears to your liking, prepare the instrumentation.*')
        if st.button("Prepare Instrumentation"):
            st.session_state.responsedata.build_instrumentation_matrix()
            st.session_state.instrmatrixbuilt = True

        if "instrmatrixbuilt" not in st.session_state:
            st.session_state.instrmatrixbuilt = False

        if st.session_state.instrmatrixbuilt:
            if st.button("View Instrumentation Matrix"):
                instrmatrix = st.session_state.responsedata.instrumentation_matrix
                st.dataframe(instrmatrix)
                if st.button("Hide Instrumentation Matrix"):
                    st.rerun()
    
    with tab_createmodel:
        st.subheader("Begin Scheduling")
        st.write("*NOTICE:* Only continue once all other information has been set to your liking.")

        # if "validation_error" in st.session_state:
        #     st.error(f"An error occurred: {st.session_state.validation_error}")
        #     if st.button("Okay"):
        #         del st.session_state.validation_error
        #         if "attempt_schedule" in st.session_state:
        #             del st.session_state["attempt_schedule"]
        #         st.rerun()
        #     st.stop()

        if st.button("Take me to the scheduler!"):
            # validation = st.session_state.responsedata.validate_st()
            # if validation != 'Success':
            #     st.error(f"An error has occurred: {validation}. Please address this before continuing.")
            #     if st.button('Okay',key='ok'):
            #         st.rerun()

            try:
                st.session_state.responsedata.validate_st()
            except Exception as e:
                st.warning(f'An Error Has Occurred: {e} Please address this before continuing.')
                if st.button('Okay'):
                    st.rerun()
                st.stop()
                


            if "schedulingmodel" not in st.session_state:
                st.session_state.schedulingmodel = SchedulingModel(st.session_state.responsedata) 
                st.success('Prepared data loaded into SchedulingModel class')
                st.session_state.tab_state = 'KickstartModel'
                st.rerun()
            else:
                if st.button('Restart Scheduler!'):
                    st.session_state.schedulingmodel = SchedulingModel(st.session_state.responsedata) 
                    st.success('Prepared data loaded into SchedulingModel class')
                    st.session_state.tab_state = 'KickstartModel'
                    st.rerun()
if (st.session_state.tab_state == 'KickstartModel' and "validation_error" not in st.session_state):

    if not st.session_state.kickstarted:
        st.write('How many combos would you like to schedule?')
        comboscount = st.number_input('Combos Count',min_value=1,max_value=10,key='combocount')
        st.session_state.schedulingmodel.comboslist = []
        mycombolist = st.session_state.schedulingmodel.comboslist
        for i in range(comboscount):
            st.write(f'What is the name of combo {i+1}?')
            comboname = st.text_input(f'Name of Combo {i+1}',key=f"combo_name_{i}")
            mycombolist.append(comboname)
        if st.button('Continue'):
            if len(mycombolist) != len(set(mycombolist)):
                st.error("Make sure all combos have distinct names!")
            elif 'Name' in mycombolist or 'Instrument' in mycombolist:
                st.error('Combos cannot be named "Name" or "Instrument!')
            else:
                st.session_state.schedulingmodel.kickstart_model_st()
                st.session_state.kickstarted = True
                st.session_state.tab_state = 'SchedulingModel'
                st.rerun()
    else:
        print('Something went wrong')

elif st.session_state.tab_state == 'SchedulingModel':

    tab_change_combos, tab_instr_con, tab_rehearsal_con, tab_combosize_con, tab_toggleables, tab_all_con, tab_solve = st.tabs([
        'Edit Combos',
        'Instrumentation',
        'Rehearsal Count',
        'Combo Sizes',
        'Global Constraints',
        'View Constraints',
        'Schedule!'
    ])

    with tab_change_combos:
        if not st.session_state.confirm_combo_reset:
            if st.button('Edit Combos to be Scheduled'):
                st.session_state.confirm_combo_reset = True
                st.rerun()
        else:
            st.warning('Resetting the combos will delete all constraints. Continue?')
            col1, col2, col3 = st.columns([1,1,10])
            with col1:
                if st.button("Yes",key='confirm_comboreset'):
                    del st.session_state.schedulingmodel
                    st.session_state.schedulingmodel = SchedulingModel(st.session_state.responsedata) 
                    st.success('Prepared data loaded into SchedulingModel class')
                    st.session_state.tab_state = 'KickstartModel'
                    st.session_state.kickstarted = False
                    st.session_state.confirm_combo_reset = False
                    st.rerun()

            with col2:
                if st.button("No",key='cancel_comboreset'):
                    st.session_state.confirm_combo_reset = False
                    st.rerun()


    with tab_instr_con:

        st.subheader('Instrumentation Constraints')
        modelclass = st.session_state.schedulingmodel
        mymodel = st.session_state.schedulingmodel.model
        if len(modelclass.instrumentationconstraints) == 0:
            st.write('No Instrumentation Constraints Yet!')
            st.session_state.no_inst_constraints = True
        else:
            st.write('**Current Instrumentation Constraints:**')
            for i,constraint in enumerate(modelclass.instrumentationconstraints):
                col1, col2 = st.columns([4,2])
                col1.write(constraint['inwords'])
                if col2.button('Delete Constraint',key=f'delete_inst_{i}'):
                    del modelclass.instrumentationconstraints[i]
                    st.rerun()
        
        if modelclass.instrumentationconstraints != modelclass.implementedinstrconstraints:
            st.warning('NOTICE: Your changes are unsaved. Select "Implement" to save them.')

        if "show_inst_constraint_builder" not in st.session_state:
            st.session_state.show_inst_constraint_builder = False

        if st.button('Write New Constraint',key='writeinst'):
            st.session_state.show_inst_constraint_builder = True
            st.write('in progress (delete this later)')
    # instrumentchoices = instrument_groups_list + instruments_list
    # combochoices = combos_list + ['All Combos']\
        if st.session_state.show_inst_constraint_builder:
            instrument_groups_list = st.session_state.schedulingmodel.instrgroupsets
            instruments_list = list(mymodel.Instruments.data())
            combos_list = list(mymodel.Combos.data())

            instrumentchoices = instrument_groups_list + instruments_list

            combochoices = ['All Combos'] + combos_list

            col1, col2, col3, col4 = st.columns([2, 2, 2, 2])

            with col1:
                combo = st.selectbox('Combo',combochoices,key='combo_instcon')
            with col2:
                bound_long = st.selectbox("Bound", ["At Least", "At Most", "Exactly"], key="bound_instcon")
            with col3:
                value = st.number_input("Instrument Count", min_value=0,max_value=20,step=1,key="value_instcon")
            with col4:
                instrument = st.selectbox("Instrument", instrumentchoices, key='instr_instcon')

            st.markdown(
                f"**Constraint:** *{combo}* must have *{bound_long.lower()}* *{value}* instrument(s) of type: *{instrument}*."
            )

            if bound_long == 'At Least':
                bound = 'LB'
            elif bound_long == 'At Most':
                bound = 'UB'
            elif bound_long == 'Exactly':
                bound = 'amt'

            wordedconstraint = f"{combo} must have {bound_long.lower()} {value} instrument(s) of type: {instrument}"

            if st.button('Add Constraint',key='add_inst'):
                instrumentation_constraint = {
                    'combo': combo,
                    'type': bound,
                    'value': value,
                    'instrument': instrument,
                    'inwords': wordedconstraint
                }
                if instrumentation_constraint in modelclass.instrumentationconstraints:
                    st.error('That constraint already exists!')
                else:
                    modelclass.instrumentationconstraints.append(instrumentation_constraint)
                    st.session_state.show_inst_constraint_builder = False
                    st.rerun()
            if st.button('Cancel',key='cancel_inst'):
                st.session_state.show_inst_constraint_builder = False
                st.rerun()
        
        st.write('---')

        if st.button('Implement Changes',key='impl_inst'):
            remove_old_constraints_st(modelclass,'instrumentation')
            modelclass.build_instrumentation_constraints()

    with tab_rehearsal_con:

        st.subheader('Rehearsal Count Constraints')
        modelclass = st.session_state.schedulingmodel
        mymodel = st.session_state.schedulingmodel.model
        if len(modelclass.rehearsalconstraints) == 0:
            st.write('No Rehearsal Constraints Yet!')
            st.session_state.no_inst_constraints = True
        else:
            st.write('**Current Rehearsal Count Constraints:**')
            for i,constraint in enumerate(modelclass.rehearsalconstraints):
                col1, col2 = st.columns([4,2])
                col1.write(constraint['inwords'])
                if col2.button('Delete Constraint',key=f'delete_reh_{i}'):
                    del modelclass.rehearsalconstraints[i]
                    st.rerun()
        
        if modelclass.rehearsalconstraints != modelclass.implementedrehearsalconstraints:
            st.warning('NOTICE: Your changes are unsaved. Select "Implement" to save them.')

        if "show_rehearsal_constraint_builder" not in st.session_state:
            st.session_state.show_rehearsal_constraint_builder = False

        if st.button('Write New Constraint',key="write_reh"):
            st.session_state.show_rehearsal_constraint_builder = True
            st.write('in progress (delete this later)')
        
        if st.session_state.show_rehearsal_constraint_builder:
            slotgroups_list = list(modelclass.slotgroupsdict.keys())
            combos_list = list(mymodel.Combos.data())

            combochoices = ['All Combos'] + combos_list

            col1, col2, col3 = st.columns([2, 2, 2])

            with col1:
                combo = st.selectbox('Combo',combochoices,key='combo_rehcon')
            with col2:
                slotgroup = st.selectbox("Rehearsal Type",slotgroups_list, key="group_rehcon")
            with col3:
                value = st.number_input("# Rehearsals", min_value=0,max_value=10,step=1,key="value_rehcon")


            st.markdown(
                f"**Constraint:** *{combo}* must rehearse in rehearsal type *{slotgroup}* *{value}* time(s) weekly."
            )

            wordedconstraint = f"{combo} must rehearse in rehearsal type {slotgroup} {value} time(s) weekly."

            if st.button('Add Constraint',key='add_reh'):
                rehearsal_constraint = {
                    'combo': combo,
                    'value': value,
                    'slotgroup': slotgroup,
                    'inwords': wordedconstraint
                }
                if rehearsal_constraint in modelclass.rehearsalconstraints:
                    st.error('That constraint already exists!')
                else:
                    modelclass.rehearsalconstraints.append(rehearsal_constraint)
                    st.session_state.show_rehearsal_constraint_builder = False
                    st.rerun()
            if st.button('Cancel',key='cancel_reh'):
                st.session_state.show_rehearsal_constraint_builder = False
                st.rerun()
        
        st.write('---')

        if st.button('Implement Changes',key='impl_reh'):
            remove_old_constraints_st(modelclass,'rehearsal')
            modelclass.build_rehearsal_constraints()

    with tab_combosize_con:
        st.subheader('Combo Size Constraints')
        modelclass = st.session_state.schedulingmodel
        mymodel = st.session_state.schedulingmodel.model
        if len(modelclass.combosizeconstraints) == 0:
            st.write('No Combo Size Constraints Yet!')
            st.session_state.no_combosize_constraints = True
        else:
            st.write('**Current Combo Size Constraints:**')
            for i,constraint in enumerate(modelclass.combosizeconstraints):
                col1, col2 = st.columns([4,2])
                col1.write(constraint['inwords'])
                if col2.button('Delete Constraint',key=f'delete_cs_{i}'):
                    del modelclass.combosizeconstraints[i]
                    st.rerun()
        
        if modelclass.combosizeconstraints != modelclass.implementedsizeconstraints:
            st.warning('NOTICE: Your changes are unsaved. Select "Implement" to save them.')

        if "show_size_constraint_builder" not in st.session_state:
            st.session_state.show_size_constraint_builder = False

        if st.button('Write New Constraint',key="write_cs"):
            st.session_state.show_size_constraint_builder = True
            st.write('in progress (delete this later)')
        
        if st.session_state.show_size_constraint_builder:

            combos_list = list(mymodel.Combos.data())
            combochoices = ['All Combos'] + combos_list

            col1, col2, col3 = st.columns([2, 2, 2])

            with col1:
                combo = st.selectbox('Combo',combochoices,key='combo_sizecon')
            with col2:
                bound_long = st.selectbox("Bound", ["At Least", "At Most", "Exactly"], key="bound_sizecon")
            with col3:
                value = st.number_input("Size", min_value=0,max_value=20,step=1,key="value_sizecon")

            st.markdown(
                f"**Constraint:** *{combo}* must have *{bound_long.lower()}* *{value}* members."
            )

            if bound_long == 'At Least':
                bound = 'LB'
            elif bound_long == 'At Most':
                bound = 'UB'
            elif bound_long == 'Exactly':
                bound = 'amt'

            wordedconstraint = f"{combo} must have {bound_long.lower()} {value} members."

            if st.button('Add Constraint',key='add_size'):
                combo_size_constraint = {
                    'combo': combo,
                    'type': bound,
                    'value': value,
                    'inwords': wordedconstraint
                }
                if combo_size_constraint in modelclass.combosizeconstraints:
                    st.error('That constraint already exists!')
                else:
                    modelclass.combosizeconstraints.append(combo_size_constraint)
                    st.session_state.show_size_constraint_builder = False
                    st.rerun()
            if st.button('Cancel',key='cancel_size'):
                st.session_state.show_size_constraint_builder = False
                st.rerun()
        
        st.write('---')

        if st.button('Implement Changes',key='impl_size'):
            remove_old_constraints_st(modelclass,'combo_size')
            modelclass.build_combo_size_constraints()

    with tab_toggleables:
        modelclass = st.session_state.schedulingmodel
        mymodel = st.session_state.schedulingmodel.model

        constraint_aliases = {
        'no_instr_repeats': 'Each combo may not have more than 1 of a given instrument',
        'one_combo_max': 'Each person may only be assigned to 1 combo',
        'no_slot_repeats': 'Each time slot may only be used for 1 combo',
        'slot_availability': 'Each person must be available for the time slot which their combo is assigned'
        }

        st.write('Note: Remember to select "Implement", even if you make no changes.') 
        st.write('\n')

        for k,v in constraint_aliases.items():
            const_col, toggle_col = st.columns([3,1])
            const_col.write(v)
            const_col.write('\n')
            toggle_col.checkbox('Enable',value=True,key=f'{k}_toggle')

        st.write('---')

        if st.button('Implement Constraints',key='global_con'):
            modelclass.build_toggle_constraints()

    with tab_all_con:
        modelclass = st.session_state.schedulingmodel
        mymodel = st.session_state.schedulingmodel.model
        for i, (k, v) in enumerate(modelclass.implementedconstraints.items(), start=1):
            k_str = f"{k:<30}" 
            v_str = f"{v}" 
            st.markdown(f"```text\n{i}. {k_str} {v_str}\n```")

    with tab_solve:
        if not st.session_state.confirm_schedule_box:
            if st.button('Schedule Combos!'):
                st.session_state.confirm_schedule_box = True
                st.rerun()
        else:
            st.warning('Are you sure? Ensure all desired constraints are implemented before continuing.')
            col1, col2, col3 = st.columns([1,1,10])
            with col1:
                if st.button("Yes",key='confirm_solve'):
                    modelclass = st.session_state.schedulingmodel
                    solved = modelclass.solve_model()
                    if solved:
                        st.session_state.ready_for_assignments = "Ready"
                    else:
                        st.session_state.ready_for_assignments = 'Unsolved'
                    st.session_state.confirm_schedule_box = False
                    st.rerun()

            with col2:
                if st.button("No",key='cancel-solve'):
                    st.session_state.confirm_schedule_box = False
                    st.rerun()
            
        if st.session_state.ready_for_assignments == 'Unsolved':
            st.error('No assignments available. Constraints are too restrictive or data was misentered.')

        if st.session_state.ready_for_assignments == 'Ready':
            modelclass = st.session_state.schedulingmodel
            combosdictionary = modelclass.get_combo_assignments()
            for combo, roster in combosdictionary.items():
                st.write(combo)
                st.dataframe(roster)
            st.write('Rehearsal Times')
            st.dataframe(modelclass.get_rehearsal_assignments())
            st.session_state.ready_for_assignments = "Ready"
            if not st.session_state.confirm_reset_constraints:
                if st.button('Change Constraints'):
                    st.session_state.confirm_reset_constraints = True
                    st.rerun()
            else:
                st.warning('All constraints will be unimplemented. Edit constraints and reimplement them before re-scheduling. Continue?')
                concol1, concol2, concol3 = st.columns([1,1,10])
                with concol1:
                    if st.button("Yes",key='confirm_reset'):
                        modelclass = st.session_state.schedulingmodel
                        for type in ['instrumentation','rehearsal','combo_size']:
                            remove_old_constraints_st(modelclass,type)
                        st.session_state.confirm_reset_constraints = False
                        st.session_state.ready_for_assignments = 'notready'
                        st.rerun()

                with concol2:
                    if st.button("No",key='cancel_reset'):
                        st.session_state.confirm_reset_constraints = False
                        st.rerun()
                

                