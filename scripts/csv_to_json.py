import copy
import json
import logging
import os
import re

import pandas as pd

final_config = {"config": {}}

csv_path = r"C:\Users\Paul\Downloads\Kurse Schulung20_21.csv (1)\Kurse Schulung20_21.csv"
logging.debug(f"Loading csv file {csv_path}")

kurs_file = pd.read_csv(csv_path)

person_colume_name = kurs_file.columns[1]
croRef_colume_name = kurs_file.columns[2]
time_colume_name = kurs_file.columns[0]

logging.debug(f"Using {person_colume_name} as person_colume_name")
logging.debug(f"Using {time_colume_name} as time_colume_name")

subject_names = list(kurs_file.columns)
subject_names.remove(person_colume_name)
subject_names.remove(time_colume_name)
subject_names.remove(croRef_colume_name)
filtered_subject_names = []
group_types = []
for name in subject_names:
    group_type = (name.split("["))[1].split("]")[0]
    name = re.sub(r"\[.*\]", "", name)[:-1]
    if name not in filtered_subject_names:
        filtered_subject_names.append(name)
    if group_type not in group_types:
        group_types.append(group_type)
subject_names = filtered_subject_names
del filtered_subject_names

logging.info(f"Found class_types {group_types}")
logging.info(f"Found subjects {subject_names}")
final_config["config"]["groupTypes"] = group_types
final_config["config"]["numGroups"] = None
final_config["config"]["subjects"] = []
for subject in subject_names:
    final_config["config"]["subjects"].append({
        "name": subject,
        "lessons_in_group_types": []
    })

colume_names = list(kurs_file.columns)
teachers_config = []
for i, teacher in kurs_file.iterrows():
    print(teacher[person_colume_name])
    preferences = []
    for subject in subject_names:
        subject_preferences = []
        for group_type in group_types:

            course_name = f"{subject} [{group_type}]"
            if course_name in colume_names:
                subject_preferences.append(int(str(teacher[course_name])[0]))
            else:
                subject_preferences.append(0)
        preferences.append(subject_preferences)
    coRef = True
    if teacher[croRef_colume_name] == "Ref":
        coRef = False
    woman = input(f"Is {teacher[person_colume_name]} an woman? Type y: ")
    if woman in ["y", "Y", "Yes", "yes"]:
        woman = True
    else:
        woman = False

    teachers_config.append({
        "name": teacher[person_colume_name],
        "shortName": teacher[person_colume_name][:3],
        "maxLessons": 10,
        "preferences": preferences,
        "coRef": coRef,
        "woman": woman
    })

final_config["teachers"] = teachers_config

config_dir = os.getcwd()
path = input(f"Root for result config [{config_dir}]:")
if path != "":
    config_dir = path
with open(os.path.join(config_dir, "csv_config2021.json"), 'w', encoding="UTF-16") as f:
    json.dump(final_config, f, indent=4, sort_keys=True, ensure_ascii=False)

logging.info("Done")