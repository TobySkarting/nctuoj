map_power = { 
    "user_manage": 1,       #modify user right
    "group_manage": 2,      #create group
    "execute_manage": 3,    #execute type
    "verdict_manage": 4,
}

map_group_power = {
    'group_manage': 1,
    "bulletin_manage": 2,      #add admin for group
    'problem_manage': 3,
    'submission_manage': 4,
    'contest_manage': 5,
}

map_lang = {
    0:  "C",
    1:  "C++",
    2:  "Java",
    3:  "Python2",
    4:  "Python3",
    5:  "Go",
    6:  "Perl",
    7:  "Javascript",
    8:  "Haskell",
    9:  "ruby",
    10: "sh",
}

map_visible = {
    0: "Invisible",
    1: "Visible",
}

map_default_file_name = {
    0: 'main.c',
    1: 'main.cpp',
    2: 'main.java',
    3: 'main.py',
    4: 'main.py',
    5: 'main.go',
    6: 'main.pl',
    7: 'main.js',
    8: 'main.hs',
    9: 'main.rb',
    10:'main.sh',
}
map_group_type = {
    -1: "Private",
     0: "Public",
     1: "Inpublic"
}
