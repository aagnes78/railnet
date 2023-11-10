#!/usr/bin/env python3
# -*-coding: utf-8 -*-

"""
File:   
Author: Agnes Gyarmati
Date:   2023-11-09
Python version: 3.8.10
Description: Small question and answer game about Belgian rail network, 
             with text-only menu and input.

"""

# for reading and handling csv input
import pandas as pd

# Network is a directed graph with station ids in the vertices,
# and routes between two stations as edges, with the distance in km as weights
# Note: distance between A-B and B-A may slightly differ, as in the Infrabel DB

class Network:
    """The rail network with stations and tracks between stations,
    also including distances (in km).
    """
    def __init__(self):
        self.stations = {}
    
    def add_station(self, station):
        assert isinstance(station, int)
        self.stations[station] = {}

    def add_track(self, source, target, distance):
        assert isinstance(source, int)
        assert isinstance(target, int)
        self.stations[source][target] = distance
    
    def write_station_raw(self, station):
        assert isinstance(station, int)
        print(station, "adjacent stations from here:", self.stations[station])
    
    def list_adjacent_stations(self, station):
        assert isinstance(station, int)
        return [*self.stations[station].keys()]
    
    def isadjacent(self, station1, station2):
        assert isinstance(station1, int)
        assert isinstance(station2, int)
        return station2 in self.stations[station1]

# TODO
#    def path_finder(self, station1, station2)


# Network works with station IDs, station names will be stored separately
network = Network()
places = {}

# File also included in the repo (extracted from Infrabel opendata DB)
tracks = pd.read_csv("station_to_station_extract.csv")

# extracting unique stations from columns 1-2 (id, name)
tracks_col12 = tracks[["source_id", "source_name"]]
tracks_stations = tracks_col12.drop_duplicates()

for label, row in tracks_stations.iterrows():
    places[row["source_id"]] = row["source_name"]
    network.add_station(row["source_id"])

for label, row in tracks.iterrows():    
    network.add_track(row["source_id"], row["target_id"], row["distance"])



def name_by_id(id_no):
    global places
    try:
        return places[id_no]
    except:
        print("places lookup: Sorry, that's not a valid station ID")


def read_id():
    your_id_string = input("Which station? Specify its ID number:\n")

    global places

    try:
        your_id = int(your_id_string)
        if your_id in places:
            return your_id
        else:
            print("Sorry, there's no station with this ID")
            return 0
    except:
        print("Sorry, not a valid ID")
        return 0


def show_menu():
    print("What you can ask for:\n")
    print("1 : identify a station by its ID number - between", smallest_id, "and", largest_id)
    print("2 : identify a station, and list where to go from there")
    print("3 : are two stations adjacent in the rail network?")
#TODO    print("4 : what's the distance between two stations?")
    print("4 : quit")


# Note: Python 3.10 introduced "switch"
#def execute_option(choice):
#    match choice:
#        case 1:
#            name_by_id(your_id())


# This works without the match-case switch
# (tried in python 3.8) 
# return value True / False is about "wanna_quit"
def execute_option(choice):
    global network
    
    if choice == '1':
        your_id = read_id()
        if your_id != 0:
            name = name_by_id(your_id)
            print(name)

    elif choice == '2':
        your_id = read_id()
        if your_id != 0:
            print("\nFrom", name_by_id(your_id), "there are direct tracks (not necessarily trains) to:\n") 
            #adj_list = network.list_adjacent_stations(your_id)
            answer_list = network.list_adjacent_stations(your_id)
            for ans in answer_list:
                answer = name_by_id(ans) + " (" + str(ans) + ") "
                #answer = name_by_id(ans)
                print(answer)
 
    elif choice == '3':
        your_id1 = read_id()
        name1 = name_by_id(your_id1)
        your_id2 = read_id()
        name2 = name_by_id(your_id2)
        if network.isadjacent(your_id1, your_id2):
            print("\n{} ({}) and {} ({}) are adjacent stations".format(name1, your_id1, name2, your_id2))
            print("(mind you, there is not necessarily a direct train between them)")
        else:
            print("{} ({}) and {} ({}) are not adjacent stations.".format(name1, your_id1, name2, your_id2))

    else:
        print("Thanks. Happy travels.")
        return True
    return False


def run_menu():
    show_menu()
    try:
        your_choice = input()
        print("You've selected:", your_choice, "\n")
        wanna_quit = execute_option(your_choice)
        if not wanna_quit:
            your_choice = input("\nDo you want to continue? yes / no\n")
            if your_choice.lower() in ['yes', 'y', 'zes']:
                run_menu()
    except:
        print("Sorry, that's not in the menu.\n")
        run_menu()


# Writing welcome message on the screen, using some data from the dataframes above
print("Welcome to the Belgian rail network!\n")
print("There are", tracks_stations.shape[0], "stations in the Infrabel database,")
print("and", tracks.shape[0], "direct routes between them.\n")

smallest_id = min(network.stations)
largest_id = max(network.stations)

print("Stations are identified by numbers between", smallest_id, "and", largest_id)
print("where", smallest_id, "is", places[smallest_id], 
      "and", largest_id, "is", places[largest_id],
      "\n\nBtw, Gent-Sint-Pieters is at 455, as GENT-ST-P")
print("(No, the IDs are not assigned in alphabetical order, as you can see.)\n")

# no need for these DataFrames any more
del tracks
del tracks_col12
del tracks_stations


run_menu()

