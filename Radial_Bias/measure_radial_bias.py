# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 12:05:22 2023

@author: Alexia Roux-Sibilon

Experiment: Radial bias 

This program measures contrast sensitivity (detection threshold) for vertical 
and horizontal gabor patches, at 4 visual field position (upper & lower vertical
meridian, left & right horizontal meridian).

- 4AFC task (observer presses either left, right, up or down arrow)


"""

#%%#   Import packages

from psychopy import core, visual, gui, data, event, monitors, sound
import numpy as np
import pandas as pd
import os
import random



#%%#  Path stuff

# Print the current working directory
print("Current working directory: {0}".format(os.getcwd()))

# Change the current working directory HERE
#cwd = os.chdir(r'C:\Users\alrouxsi\Documents\Rprojects\2023_iTRAC (Marius)\measure_radial_bias')
cwd = os.chdir(r'C:/Users/humanvisionlab/Documents/Marius/measure_radial_bias')

print("Current working directory: {0}".format(os.getcwd()))
cwd = format(os.getcwd())

stimdir = cwd + '\stim\\' #directory where the stimuli are 
datadir = cwd + '\data\\' #directory to save data in



#%%#
'''
Open dlg box, Store info about the experiment session
'''

# Get subject's info through a dialog box
exp_name = 'measure_radialbias'
exp_info = {
    'participant': '',
    'session': '',
    'screendistance(cm)': '90',
    'eccentricity (15° or 20°, default is 15)': 15,
    'gabor patch size (3° or 6°, default is 6)': 6,
    'gabor patch spatial frequency (default is 4cpd)': 4,
    'practice': ('yes','no') #whether to do the practice (yes or no). Can be set to "no"
                     #if we just want to check the test loop. When testing participants,
                     #it should be set to "yes"
    }

dlg = gui.DlgFromDict(dictionary = exp_info, title = exp_name) # Open a dialog box
if dlg.OK == False: # If 'Cancel' is pressed, quit
    core.quit()
        
# Get variables from the dial box
exp_info['date'] = data.getDateStr()
exp_info['exp_name'] = exp_name
participant = exp_info['participant']
date = exp_info['date']
eccentricity = exp_info['eccentricity (15° or 20°, default is 15)']
gaborSizeDVA = exp_info['gabor patch size (3° or 6°, default is 6)']
gaborSFDVA = exp_info['gabor patch spatial frequency (default is 4cpd)']
practice = exp_info['practice']





#%%#
'''
Define / initialize some variables 
'''

# Define parameters of the Gabor patch stimulus (parameters valid for eye-screen distance = 90cm)
if eccentricity == 15:
    # Where to present the stim (eccentricity)
    left_xpos = -752
    right_xpos = 752
    up_ypos = 752
    down_ypos = -752
elif eccentricity == 20:
    # Where to present the stim (eccentricity)
    left_xpos = -1008
    right_xpos = 1008
    up_ypos = 1008
    down_ypos = -1008
else:
    core.quit()
    print('Choose an eccentricity of either 15 or 20')

if gaborSizeDVA == 3:
    gaborSize = 150 # Size in pixels 
elif gaborSizeDVA == 6:
    gaborSize = 299 # Size in pixels
else:
    core.quit()
    print('Choose a size for the gabor patch of either 3 or 6')
    
if gaborSFDVA == 4:
    gaborSF = 0.1980 # Size in pixels 
else:
    core.quit()
    print('Parameters are only set for a spatial frequency of 4 cpd. Add others to the code if you want to test with another SF')
    

# Presentation duration
stimDuration = 0.150 

# Number of practice trials
nPracticeTrials = 10

# Number of trials that we want for each condition (e.g., condition [VF = left, orientation = horizontal])
nTrialsPerStaircase = 55 # should probably be at least 50 or 60

# max time (in s) to wait for a response
timelimit = 3

# fixation colors
neutralColor = (-1, -1, -1)
waitColor    = (-0.2, -0.2, -0.2) #for when waiting for a response
notOKcolor   = (-1, 0.7, -1) 
OKcolor      = (0.7, -1, -1) #both these colors look weird with the texture that
                             #makes the fixation, but it is ok (notOKcolor is pinkish, OKcolor is blueish)


# Initialise these variables
thisTrial = 0
trial = 0 # this is just trial number, to append to data file
    
# High contrasts levels, for the test phase 
highContrastLevels = np.around(list(np.arange(0.7,1,0.01)),3)
highContrastLevels = highContrastLevels.tolist()    
np.random.shuffle(highContrastLevels)

# size of the gaussian background
bgSize = 3299


#%%#
'''
Prepare window object and stimuli
'''
# Window object
###############
OLED = monitors.Monitor('testMonitor') #this is default 2.2 gamma
OLED.setSizePix((3840, 2160)) 
win = visual.Window(monitor = OLED,
                    color = (-1, -1, -1),
                    units = 'pix',
                    fullscr = True,
                    allowGUI = True)
win.setMouseVisible(False)

# Fixation dot
##############
fix = np.ones((20, 20))*(-1)
fixation = visual.GratingStim(win, tex=fix, mask='gauss', units='pix', size=20)    

# Little Bip sound 
##################
bleepf = os.path.join(stimdir + 'blip.wav')
bleep = sound.Sound(value=bleepf)
bleep.setVolume(0.1)

# Pause text
############
pause = visual.TextStim(win, color = (-1, -1, -0.5))

# Gaussian Gray background
##########################
gaussianGrayf = os.path.join(stimdir + 'gaussianGray.bmp') 
gaussianGray = visual.ImageStim(win, image = gaussianGrayf,
                                units = 'pix', pos = (0,0), 
                                size = (bgSize,bgSize))

# Little gabor patch stimulus
##########################
# Create base object to host the different versions of the gabor stimulus
#lilGabor = visual.GratingStim(win, units = 'pix',
                              #sf = gaborSF, mask = 'gauss') 

lilGabor = visual.GratingStim(win, units = 'pix',
                              sf = gaborSF, mask = 'gauss', size = gaborSize) 


#%%#
'''
Make trial list for this subject.
(on the first session. On the next sessions, the pickled trial list will be loaded)
'''

#%%#  Experimental design
VFs = ['left','right','up','down']
orientations = ['horizontal','vertical']
#stimconditions = ['gabor','slope10', 'slope15', 'slope20']
#patchExamplars = [1,2,3,4,5,6,7,8,9,10]


triallist = []
for VF in VFs:
    for ori in orientations:
        tmp_dict = {'VF':VF, 'ori':ori}
        triallist.append(tmp_dict)

for i in range(int(nTrialsPerStaircase)-1):
    condition_template = []
    for VF in VFs:
        for ori in orientations:
            tmp_dict = {'VF':VF, 'ori':ori}
            condition_template.append(tmp_dict)
    triallist.extend(condition_template)
random.shuffle(triallist)


# nb trials...
nTrialsTotal = len(triallist)
totalTime = nTrialsTotal*3/60/60 #approximative total time in hours


#%%#
'''
Prepare staircases
'''
#  Define Staircase parameters
##############################

ndown = 2 # Nb of correct responses before decreasing the contrast
nup = 1 # Nb of incorrect responses before increasing the contrast
down_step = 0.02
up_step = 0.02
maxContrast = 0.25

# initializes some dictionaries used by the staircase() function
################################################################
thisCond = [] 
condition_names = ['left_horizontal', 'left_vertical',
                   'right_horizontal', 'right_vertical',
                   'up_horizontal', 'up_vertical',
                   'down_horizontal', 'down_vertical'
                   ]

value = 0
contrast_dict    = {key:maxContrast for key in condition_names}
acc_count_dict   = {key:value for key in condition_names}
trial_count_dict = {key:value for key in condition_names}


#  Define staircase function
############################

def staircase(condition):
    # we need to work with the global variables (so that they can be used 
    # outside of the function)
    global thisCond
    global contrast_dict
    global acc_count_dict
    global trial_count_dict
  

    # 1st trial: set the initial contrast value as the value defined in maxContrast
    if trial_count_dict[thisCond] == 1: 
        contrast_dict[thisCond] = contrast_dict[thisCond]
    
    # From the 2nd trial:
    elif trial_count_dict[thisCond] > 1: 
        
            # if acc = 0 at last trial, increases contrast level
            if acc_count_dict[thisCond] == 0: 
                contrast_dict[thisCond] = abs(contrast_dict[thisCond] + up_step)
            # if acc = 1 at last trial, first time, keep the same contrast level
            elif (acc_count_dict[thisCond] > 0) & (acc_count_dict[thisCond] < ndown): 
                contrast_dict[thisCond] = abs(contrast_dict[thisCond]) 
            # if acc = 1 at last trial, second time, decrease contrast level
            else: # (acc_count_dict[thisCond] == ndown):
                contrast_dict[thisCond] = abs(contrast_dict[thisCond] - down_step)
                acc_count_dict[thisCond] = 0  
                

#%%#
'''
BEGIN EXPERIMENT
'''

# Draw the windows onto the screen
win.flip()


'''
INSTRUCTIONS AND PRACTICE
'''
textpage = visual.TextStim(win, height=30, alignHoriz='center', wrapWidth=1000)

instructiontexts = {
    1 : """Bienvenue ! \n \n Ajustez la position du siège et de la mentonière pour être confortablement assis. \n \n
            Appuyez sur ESPACE pour continuer.""",
    2 : """Cette expérience a pour but d’étudier l'acuité visuelle en vision périphérique, c’est-à-dire la vision sur les côtés du champ visuel. \n \n \n 
            Appuyez sur ESPACE pour continuer.""",
    3 : """Pendant l'expérience, il vous est demandé de fixer un point au centre de l'écran, et de ne jamais le lacher du regard. \n
            Un stimulus non identifiable apparaitra brièvement à droite, à gauche, en haut ou en bas de l'écran.\n 
            Votre tâche est simple, vous devez indiquer où le stimulus est apparu en utilisant les 4 flêches du clavier. \n \n \n
            Appuyez sur ESPACE pour continuer. """,
    4 : """A certains essais, vous verrez bien le stimulus, à d'autres il sera presque invisible. Même si vous ne pouvez pas le voir clairement, faîtes de votre mieux pour deviner où le stimulus est apparu. \n \n \n 
            Appuyez sur ESPACE pour faire un test."""}

for text in instructiontexts:
    instructions = textpage
    instructions.text = instructiontexts[text]
    gaussianGray.draw()
    instructions.draw()
    win.flip()
    event.clearEvents()
    keys = event.waitKeys(keyList=['space', 'q'])
    if 'q' in keys:
        win.close()
        core.quit()
    elif 'space' in keys :
        continue
win.flip(clearBuffer=True)
core.wait(1)


# Contrasts levels, just for this litle practice phase 
contrastLevels = np.around(list(np.arange(0.1,0.5,0.01)),3)
contrastLevels = contrastLevels.tolist()      

if practice == 'yes':
    for practicetrial in range(nPracticeTrials):
      
        # Draw fixation
        gaussianGray.draw()
        fixation.color = neutralColor
        fixation.draw()
        win.flip()
        core.wait(2) # wait for 2 sec
        
        # Pick a random stimulus condition
        theVF = random.choice(VFs) 
        theOri = random.choice(orientations) 

        # Set stim position
        if (theVF == 'left'):
            yPos = 0 # horizontal meridian --> y = 0
            xPos = left_xpos
        elif (theVF == 'right'):
            yPos = 0 # horizontal meridian --> y = 0
            xPos = right_xpos
        elif (theVF == 'up'):
            xPos = 0 # vertical meridian --> x = 0
            yPos = up_ypos
        elif (theVF == 'down'):
            xPos = 0 # vertical meridian --> x = 0
            yPos = down_ypos
        lilGabor.pos = (xPos,yPos)
    
        # Set stim orientation
        if theOri == 'horizontal':
            ori = 90
        elif theOri == 'vertical':
            ori = 0      
        lilGabor.ori = ori
                    
        # Set stim contrast 
        zecontrast = random.choice(contrastLevels)
        lilGabor.contrast = zecontrast
               
        # Draw stimulus
        gaussianGray.draw()
        bleep.play()
        lilGabor.draw()
        fixation.draw()
        win.flip()
        core.wait(stimDuration) 
        gaussianGray.draw()
        fixation.color = waitColor
        fixation.draw()
        win.flip()
        event.clearEvents()
        keys = event.waitKeys(maxWait=timelimit, keyList=['left', 'right', 'up', 'down', 'q'])
    
    
        # If a key is pressed, take the response. If not, just remove the images from the screen    
        if keys:
            resp = keys[0]
                                        
            #At this point, there are still no keys pressed. So "if not keys" is definitely 
            #going to be processed.
            #After removing the images from the screen, still listening for a keypress. 
            #Record the reaction time if a key is pressed.
                                        
        if not keys:
            keys = event.waitKeys(maxWait = timelimit, keyList=['left', 'right', 'up', 'down', 'q'])
                                            
        # If the key is pressed analyze the keypress.
        if keys:
            if 'q' in keys:
                break
            else:
                resp = keys[0]
        else: 
            resp = 'noResp'
            
        # Check accuracy
        if resp == theVF:
            acc = 1
        elif resp == 'noResp':
            acc = 0
        else:
            acc = 0
        
        # ISI ... (+ change fixation dot color depending on accuracy)
        if acc == 1:
            accColor = OKcolor
        else:
            accColor = notOKcolor
            
        gaussianGray.draw()
        fixation.color = accColor
        fixation.draw()
        win.flip()
        core.wait(0.5) # wait for 2 sec        
    

        if (practicetrial == nPracticeTrials-1):
            instructions = textpage
            instructions.text = """ Vous êtes maintenant prêt-e à commencer. \n \n 
                                    Appuyez sur ESPACE pour commencer."""
            gaussianGray.draw()
            instructions.draw()
            win.flip()
            event.clearEvents()
            keys = event.waitKeys(keyList=['space', 'q'])
            if 'q' in keys:
                win.close()
                core.quit()
            elif 'space' in keys:
                continue
            
            win.flip(clearBuffer=True)
            core.wait(1)



'''
TEST LOOP
'''

# Initialize output arrays

trainingtest_array = []
trial_array = []
xPos_array = []
yPos_array = []
meridian_array = []
contrast_array = []
ori_array = []
VF_array = []
resp_array = []
accuracy_array = []
accCount_array = []
thisCond_array = []
trialCount_array = []
contrastRule_array = []



win.flip()
trial = 0


for thisTrial in range(len(triallist)): 
      
        trial = trial + 1
        theTrial = triallist[thisTrial]
        theVF = theTrial['VF']
        theOri = theTrial['ori']
        thisCond = theVF + '_' + theOri 
        trial_count_dict[thisCond] = trial_count_dict[thisCond] + 1
        if (theVF == 'left') or (theVF == 'right'):
            theMeridian = "meridianH"
        else:
            theMeridian  = "meridianV"
            
        # Set stim position
        if (theVF == 'left'):
            yPos = 0 # horizontal meridian --> y = 0
            xPos = left_xpos
        elif (theVF == 'right'):
            yPos = 0 # horizontal meridian --> y = 0
            xPos = right_xpos
        elif (theVF == 'up'):
            xPos = 0 # vertical meridian --> x = 0
            yPos = up_ypos
        elif (theVF == 'down'):
            xPos = 0 # vertical meridian --> x = 0
            yPos = down_ypos
        lilGabor.pos = (xPos,yPos)
    
        # Set stim orientation
        if theOri == 'horizontal':
            ori = 90
        elif theOri == 'vertical':
            ori = 0                  
        lilGabor.ori = ori
                    
        # Set stim contrast 
        # either pick within higher contrast range
        if (thisTrial%5 == 0):
            zecontrast = random.choice(highContrastLevels)
            lilGabor.contrast = zecontrast           
            contrast_array.append(zecontrast)
            contrastRule_array.append("highCont")  
        # or use staircase rules      
        else:
            staircase(thisCond)
            lilGabor.contrast = abs(contrast_dict[thisCond])            
            contrast_array.append(contrast_dict[thisCond])
            contrastRule_array.append("staircase")
    
    
        ''' Draw stimuli on screen '''
        # Draw fixation
        gaussianGray.draw()
        fixation.color = neutralColor
        fixation.draw()
        win.flip()
        core.wait(0.5) # wait for 500ms
            
        # Draw stimulus
        gaussianGray.draw()
        bleep.play()
        lilGabor.draw()
        fixation.draw()
        win.flip()
        core.wait(stimDuration) 
        gaussianGray.draw()
        fixation.color = waitColor
        fixation.draw()
        win.flip()
        event.clearEvents()
        keys = event.waitKeys(maxWait=timelimit, keyList=['left', 'right', 'up', 'down', 'q'])
    
    
        ''' Take response, calculate accuracy and give feedback (fixation color) '''
         # If a key is pressed, take the response. If not, just remove the images from the screen    
        if keys:
            resp = keys[0]                                        
            #At this point, there are still no keys pressed. So "if not keys" is definitely 
            #going to be processed.
            #After removing the images from the screen, still listening for a keypress. 
            #Record the reaction time if a key is pressed.                                        
        if not keys:            
            keys = event.waitKeys(maxWait=timelimit, keyList=['left', 'right', 'up', 'down', 'q'])   
                                  
        # If the key is pressed analyze the keypress.
        if keys:
            if 'q' in keys:
                break
                win.close()
                core.quit()
            else:
                resp = keys[0]
        else: 
            resp = 'noResp'
            
        # Check accuracy
        if resp == theVF:
            acc = 1
            acc_count_dict[thisCond] = acc_count_dict[thisCond] + 1
        elif resp == 'noResp':
            acc = 0
            acc_count_dict[thisCond] = 0
        else:
            acc = 0
            acc_count_dict[thisCond] = 0
        
        # ISI ... (+ change fixation dot color depending on accuracy)
        if acc == 1:
            accColor = OKcolor
        else:
            accColor = notOKcolor
        
        gaussianGray.draw()
        fixation.color = accColor
        fixation.draw()
        win.flip()
        core.wait(0.5) # wait 
        gaussianGray.draw()
        fixation.color = neutralColor
        fixation.draw()
        win.flip()
        core.wait(1) # wait 
                
        
        ''' Save information about the trial '''
        trainingtest_array.append('test')
        trial_array.append(trial)
        xPos_array.append(xPos)
        yPos_array.append(yPos)
        meridian_array.append(theMeridian)
        ori_array.append(theOri)
        VF_array.append(theVF)
        resp_array.append(resp)
        accuracy_array.append(acc)
        accCount_array.append(acc_count_dict[thisCond])
        thisCond_array.append(thisCond)
        trialCount_array.append(trial_count_dict[thisCond])
    
    
        ''' Should we make a small break? ''' 
        if (trial%25 == 0):
            # PAUSE
            progression = thisTrial*100/nTrialsTotal
            pause_txt = "Vous pouvez faire une petite pause \n  \nVous avez terminé " + str(round(progression,2)) + '%' + " de l'experience \n \n Appuyez sur ESPACE pour continuer."
            pause.setText(pause_txt)
            gaussianGray.draw()
            pause.draw()
            win.flip() 
            event.clearEvents()
            keys = event.waitKeys(keyList=['space', 'q'])
            if 'q' in keys:
                break
                win.close()
                core.quit()
            if 'space' in keys:
                gaussianGray.draw()
                win.flip()
                core.wait(2)
            
win.close()


#%%#
'''
Save data and pickle some objects for the next session
'''

if not os.path.isdir(datadir):
    os.makedirs(datadir)
data_fname = exp_name + '_' + exp_info['participant']+ '_session'+ exp_info['session'] + '_' + exp_info['date'] + '.csv'
data_fname = os.path.join(datadir, data_fname)
participant = exp_info['participant']
exp_date = exp_info['date']


actualNtrials = len(contrastRule_array)
eccentricityDVA = right_xpos 

subject_array = []
exp_name_array = []
date_array = [] 
session_array = []
eccentricity_array = [] 
eccentricityDVA_array = []
gaborSize_array = []
gaborSizeDVA_array = []
gaborSF_array = []
gaborSFDVA_array = []

for n in range(actualNtrials):
    subject_array.append(participant)
    exp_name_array.append(exp_name)
    date_array.append(exp_info['date'])
    session_array.append(exp_info['session'])
    eccentricity_array.append(eccentricity)
    eccentricityDVA_array.append(eccentricityDVA)
    gaborSize_array.append(gaborSize)
    gaborSizeDVA_array.append(gaborSizeDVA)
    gaborSF_array.append(gaborSF)
    gaborSFDVA_array.append(gaborSFDVA)
    
    

output_file = pd.DataFrame({'participant': subject_array,
                            'exp_name': exp_name_array,
                            'date': date_array,
                            'session': session_array,
                            'eccentricity': eccentricity_array,
                            'eccentricityDVA': eccentricityDVA_array,
                            'gaborSize': gaborSize_array,
                            'gaborSizeDVA': gaborSizeDVA_array,
                            'gaborSF': gaborSF_array,
                            'gaborSFDVA': gaborSFDVA_array,                            
                            'training-test': trainingtest_array,
                            'trial': trial_array,
                            'xPosition': xPos_array,
                            'yPosition': yPos_array,
                            'meridian': meridian_array,
                            'contrast': contrast_array,
                            'ori': ori_array,
                            'VF': VF_array,
                            'resp': resp_array,
                            'accuracy': accuracy_array,
                            'accCount': accCount_array,
                            'condition': thisCond_array,
                            'trialCount': trialCount_array,
                            'contrastRule': contrastRule_array
                            })

# save the csv file + pickle

# CSV file
output_file.to_csv(data_fname, index = False)

   
print('FILES SAVED')

