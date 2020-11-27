import copy
import json
import logging
import os
import re

import pandas as pd

import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("file_path", type=Path)
p = parser.parse_args()
print(p.file_path, type(p.file_path), p.file_path.exists())

default_json_path = os.path.join(os.path.dirname(__file__), "basic_config.json")
with open(default_json_path) as f:
    d = json.load(f)
    final_config = d

json_path = str(p.file_path.parent / p.file_path.stem) + str(".json")
logging.debug(f"Loading csv file {str(p.file_path)}")

kurs_file = pd.read_csv(p.file_path)

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
    group_type = ((name.split("["))[1].split("]")[0])[0]
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
if "numGroups" not in final_config["config"]:
    final_config["config"]["numGroups"] = None
else:
    print("Using default num groups")
if "subjects" not in final_config["config"]:
    final_config["config"]["subjects"] = []
    for subject in subject_names:
        final_config["config"]["subjects"].append({
            "name": subject,
            "lessons_in_group_types": []
        })
else:
    default_subject_names  = [subject["name"] for subject in final_config["config"]["subjects"]]
    for new_name, default_name in zip(subject_names, default_subject_names):
        if new_name != default_name:
            raise Exception(f"Maybe the order of subjects is not the same as in the default config: {new_name} and {default_name}")
    print("Using default  subjects")


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

with open(json_path, 'w', encoding="UTF-8") as f:
    json.dump(final_config, f, indent=4, sort_keys=True, ensure_ascii=False)

logging.info("Done")