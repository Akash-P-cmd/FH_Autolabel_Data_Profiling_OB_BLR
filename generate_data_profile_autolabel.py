import os
from os import listdir, walk, makedirs
from os.path import join, isfile, exists, split, splitext
import openpyxl
import pandas as pd
import numpy as np 

base_source_folder = "/mnt/hd2/Akash/Data_profile/Base_folder"
data_info_file_name = "./data_compiled_corrected.xlsx"
base_output_folder = "./analysis_guidance_final"

    
    
def search_files(base_folder, search_keyword):
    file_list = [] 
    for root, dirs, files in walk(base_folder):
        for file in files:
            if search_keyword in file:
                file_list.append(join(root, file))
    return file_list

def write_to_excel(data_info, output_folder, file_name):
    df1 = pd.DataFrame(data_info).T
    df1.to_excel(join(output_folder, file_name))
    print ("Written Xcel: ", join(output_folder, file_name))
def make_dirs(folder):
    if not exists(folder):
        makedirs(folder)
        
def if_not_present(file_info, file):
    file_info[file] = {}
    file_info[file]["count"] = 0
    file_info[file]["ga"] = 0
    file_info[file]["bmi"] = 0
    file_info[file]["SUBJECT_AGE_GROUP"] = 0
    file_info[file]["Transducer_Data"] = 0
    file_info[file]["Processing_Function"] = 0
    file_info[file]["Manufacturer_Model_Name"] = 0
    file_info[file]["Condition"] = 0
    file_info[file]["Estimated_Fetal_Weight(EFW)(grams)"] = 0
    file_info[file]["Estimated_Fetal_Weight(EFW)(%)"] = 0         
    return file_info


        
def main():
    df = pd.read_excel(io=data_info_file_name)
    excel_data_info_list = np.squeeze(df.iloc[:, [0]].to_numpy())
    
    #print(excel_data_info_list)
    txt_training_file_path_list = search_files(join(base_source_folder, "training_files"), ".txt")
    print (txt_training_file_path_list)
    for txt_training_file_path in txt_training_file_path_list:
        # if "val.txt" in txt_training_file_path:
            # print ("Skipping...", txt_training_file_path)
            # continue
        print(txt_training_file_path)
        read = open(txt_training_file_path)
        training_file_list = read.readlines()
        file_count = {}
        for training_file in training_file_list:
            print (training_file)
            #print ()
            found = False 
            for i, file in enumerate(excel_data_info_list):
                #print (file, training_file, file in training_file)
                if file in training_file:
                    found = True
                    if file not in file_count.keys():
                        file_count = if_not_present(file_count, file)
                        file_count[file]["ga"] = df.iloc[i][1]
                        file_count[file]["bmi"] = df.iloc[i][2]
                        file_count[file]["SUBJECT_AGE_GROUP"] = df.iloc[i][3]
                        file_count[file]["Transducer_Data"] = df.iloc[i][4]
                        file_count[file]["Processing_Function"] = df.iloc[i][5]
                        file_count[file]["Manufacturer_Model_Name"] = df.iloc[i][6]  
                        file_count[file]["Condition"] = df.iloc[i][7]
                        file_count[file]["Estimated_Fetal_Weight(EFW)(grams)"] = df.iloc[i][8]
                        file_count[file]["Estimated_Fetal_Weight(EFW)(%)"] = df.iloc[i][9]                        
                                             

                    file_count[file]["count"] += 1
                    label = split(split(training_file)[0])[1]
                    name = split(training_file)[1]
                    #print ("Found: ", name, label)



                    # print(i, label, file, file_count[file])
                    # print (df.iloc[i])
                    # print ()
                    
            if not found: #RUMA Study
                name = split(training_file)[1]
                label = split(split(training_file)[0])[1]
                #print ("Not found: ", name, label)
            
                if name[:2] == "fl":
                    file_name = name[3:].split("_cleaned")[0][-11:-5]
                    if file_name not in file_count.keys():
                        file_count = if_not_present(file_count, file_name)
                    file_count[file_name]["count"] += 1
                    file_count[file_name]["fl_aug"] += 1
                    

                else:  
                    file_name = name.split("_cleaned")[0][-11:-5]
                    if file_name not in file_count.keys():
                        file_count = if_not_present(file_count, file_name)
                    file_count[file_name]["count"] += 1
                    

                    #print ("RUMA: ", file_name)
                #print(name, label, file_name, file_count[file_name])
                #print()
                #print (name)
        print (file_count)
        path, file_training = split(txt_training_file_path)
        file_name = "Guidance_" + split(path)[1] + "_" + splitext(file_training)[0] + ".xlsx"
        #output_folder = join(base_output_folder, split(path)[1])
        output_folder = base_output_folder
        make_dirs(output_folder)
        write_to_excel(file_count, output_folder, file_name)
        print ()
        #return 
                        
#main()                    
if __name__ == "__main__":
    main()
