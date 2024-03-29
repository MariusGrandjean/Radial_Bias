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
import math

#%%#  Path stuff

# Print the current working directory
print("Current working directory: {0}".format(os.getcwd()))

# Change the current working directory HERE
#cwd = os.chdir(r'C:\Users\alrouxsi\Documents\Rprojects\2023_iTRAC (Marius)\measure_radial_bias')
cwd = os.chdir(r'C:/Users/humanvisionlab/Documents/Marius/measure_radial_bias')
#cwd = os.chdir(r'C:/Users/grandjeamari/Documents/Travail/UCLouvain/PhD/Projet/Projet-Saccades/Tasks/Radial_Bias/Radial_Bias')

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
    'screenwidth(cm)': '120',
    'screenresolutionhori(pixels)': '3840', 
    'screenresolutionvert(pixels)': '2160',
    'refreshrate(hz)': '59',
    'eccentricity (15° or 20°, default is 15)': 15,
    'gabor patch size': 6,
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
gaborSizeDVA = exp_info['gabor patch size']
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

# if gaborSizeDVA == 3:
#     gaborSize = 150 # Size in pixels 
# elif gaborSizeDVA == 6:
#     gaborSize = 299 # Size in pixels
# else:
#     core.quit()
#     print('Choose a size for the gabor patch of either 3 or 6')
    
if gaborSFDVA == 4:
    gaborSF = 0.1980 # Size in pixels 
    #gaborSF = 0.02

else:
    core.quit()
    print('Parameters are only set for a spatial frequency of 4 cpd. Add others to the code if you want to test with another SF')
    

# Presentation duration
stimDuration = 0.150 

# Number of practice trials
nPracticeTrials = 10

# Number of trials that we want for each condition (e.g., condition [VF = left, orientation = horizontal])
nTrialsPerStaircase = 65 # should probably be at least 50 or 60 --> 65 for better data

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

#initialize timer
timer = core.Clock()
#%%#
'''
Prepare window object and stimuli
'''
# Window object
###############

OLED = monitors.Monitor('testMonitor') #this is default 2.2 gamma
OLED.setWidth(float(exp_info['screenwidth(cm)'])) # Cm width
OLED.setDistance(float(exp_info['screendistance(cm)']))
horipix = float(exp_info['screenresolutionhori(pixels)'])
vertpix = float(exp_info['screenresolutionvert(pixels)'])
framerate = exp_info['refreshrate(hz)']
scrsize = (horipix,vertpix)
framelength = 1000/(float(framerate))
OLED.setSizePix(scrsize)
#OLED.setSizePix((1920, 1200)) 
win = visual.Window(monitor = OLED,
                    color = "grey",
                    units = 'pix',
                    fullscr = True,
                    allowGUI = True)
win.setMouseVisible(False)

# %% Calculation of grating_size

# Constants for the calculation
d = float(exp_info['screendistance(cm)'])  # eye-screen distance in cm
dd = 2 * d  # 2*d
pixelPitch = 0.315  # pixel size in mm (to change depending on your screen)
screenWidthPix = float(exp_info['screenresolutionhori(pixels)'])  # screen width in pixels
screenHeightPix = float(exp_info['screenresolutionvert(pixels)']) # screen height in pixels

# Calculate screen width and height in cm
screenWidthCm = pixelPitch * screenWidthPix / 10  # screen width in cm
screenHeightCm = pixelPitch * screenHeightPix / 10  # screen height in cm

# Desired angular size (width and height) in degrees
alphaW = float(exp_info['gabor patch size'])
alphaH = float(exp_info['gabor patch size'])

# Calculate image width and height in cm for the desired angular size
real_hori = dd * math.tan(math.radians(alphaW / 2))  # image width in cm = 2dtan(alpha/2)
real_vert = dd * math.tan(math.radians(alphaH / 2))  # image height in cm = 2dtan(alpha/2)

# Calculate image width and height in pixels for the desired size
real_hori_pix = round(real_hori * screenWidthPix / screenWidthCm)  # image width in pixels
real_vert_pix = round(real_vert * screenWidthPix / screenWidthCm)  # image height in pixels

#gaborSizeDVA = (real_hori_pix, real_vert_pix)
gaborSizeDVA = real_hori_pix #only using hori or vert works as the target is a circle

# Fixation dot
##############
fix = np.ones((20, 20))*(-1)
fixation = visual.GratingStim(win, tex=fix, mask='gauss', units='pix', size=20)    

# Little Bip sound 
##################
bleepf = os.path.join(stimdir + 'blip.wav')
bleep = sound.Sound(value=bleepf)
bleep.setVolume(0.01)

# Pause text
############
pause = visual.TextStim(win, color = (-1, -1, -0.5))

# Gaussian Gray background
##########################
#gaussianGrayf = os.path.join(stimdir + 'gaussianGray.bmp') 
#gaussianGray = visual.ImageStim(win, image = gaussianGrayf,
#                                units = 'pix', pos = (0,0), 
#                                size = (bgSize,bgSize))


# lilGabor = visual.GratingStim(win, units = 'pix',
#                               sf = gaborSF, mask = 'gauss', size = gaborSizeDVA)

lilGabor = visual.GratingStim(win, units = 'pix',
                              sf = gaborSF, mask = 'raisedCos', size = gaborSizeDVA)  
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
textpage = visual.TextStim(win, pos= [0,0], height=30, alignHoriz='center', wrapWidth=1000)

instructiontexts = {
    1 : """Bienvenue ! \n \n Ajustez la position du siège et de la mentonière pour être confortablement assis. \n \n
            Appuyez sur ESPACE pour continuer.""",
    2 : """Cette expérience a pour but d’étudier l'acuité visuelle en vision périphérique, c’est-à-dire la vision sur les côtés du champ visuel. \n \n
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
    #gaussianGray.draw()
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
        #gaussianGray.draw()
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
        #gaussianGray.draw()
        bleep.play()
        lilGabor.draw()
        fixation.draw()
        win.flip()
        core.wait(stimDuration) 
        #gaussianGray.draw()
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
            
        #gaussianGray.draw()
        fixation.color = accColor
        fixation.draw()
        win.flip()
        core.wait(0.5) # wait for 2 sec        
    

        if (practicetrial == nPracticeTrials-1):
            instructions = textpage
            instructions.text = """ Vous êtes maintenant prêt-e à commencer. \n \n 
                                    Appuyez sur ESPACE pour commencer."""
            #gaussianGray.draw()
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



#%%
# Test loop #


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
RT_array = []

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
        #gaussianGray.draw()
        fixation.color = neutralColor
        fixation.draw()
        win.flip()
        core.wait(0.5) # wait for 500ms
            
        # Draw stimulus
        #gaussianGray.draw()
        bleep.play()
        lilGabor.draw()
        fixation.draw()
        win.flip()
        core.wait(stimDuration) 
        #gaussianGray.draw()
        fixation.color = waitColor
        fixation.draw()
        win.flip()
        timer.reset()
        event.clearEvents()
        keys = event.waitKeys(maxWait=timelimit, keyList=['left', 'right', 'up', 'down', 'q'])
    
        ''' Take response, calculate accuracy and give feedback (fixation color) '''
         # If a key is pressed, take the response. If not, just remove the images from the screen    
        if keys:
            resp = keys[0]
            time = timer.getTime()                                        
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
            time = timelimit
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
        
        #gaussianGray.draw()
        fixation.color = accColor
        fixation.draw()
        win.flip()
        core.wait(0.5) # wait 
        #gaussianGray.draw()
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
        RT_array.append(time)
        accCount_array.append(acc_count_dict[thisCond])
        thisCond_array.append(thisCond)
        trialCount_array.append(trial_count_dict[thisCond])
    
    
        ''' Should we make a small break? ''' 
        if (trial % 25 == 0):
            # PAUSE
            progression = thisTrial*100/nTrialsTotal
            # Calculate mean_accuracy based on the last 25 trials
            # Ensure there are at least 25 trials completed before calculating
            if trial >= 25:
                last_25_trials_accuracy = accuracy_array[-25:]
                mean_accuracy = np.mean(last_25_trials_accuracy) * 100
            else:
                mean_accuracy = np.mean(accuracy_array) * 100 # Fallback to overall accuracy for the first 25 trials
            if mean_accuracy >= 50:
                pause = visual.TextStim(win, color = "green")
            else:
                pause = visual.TextStim(win, color = "red")
            pause_txt = "Votre score est de " + str(round(mean_accuracy,2))+'%.'+"\n\n\nVous pouvez faire une petite pause. \n  \nVous avez terminé " + str(round(progression,2)) + '%' + " de l'experience. \n \n "+" \n \n Appuyez sur ESPACE pour continuer."
            pause.setText(pause_txt)
            #gaussianGray.draw()
            pause.draw()
            win.flip() 
            event.clearEvents()
            keys = event.waitKeys(keyList=['space', 'q'])
            if 'q' in keys:
                break
                win.close()
                core.quit()
            if 'space' in keys:
                #gaussianGray.draw()
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
#gaborSize_array = []
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
    gaborSizeDVA_array.append(gaborSizeDVA)
    gaborSF_array.append(gaborSF)
    gaborSFDVA_array.append(gaborSFDVA)
    
    

output_file = pd.DataFrame({'participant': subject_array,
                            'exp_name': exp_name_array,
                            'date': date_array,
                            'session': session_array,
                            'eccentricity': eccentricity_array,
                            'eccentricityDVA': eccentricityDVA_array,
                            'gaborSizeDVA': gaborSizeDVA_array,
                            #'gaborSF': gaborSF_array,
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
                            'rt': RT_array,
                            'accCount': accCount_array,
                            'condition': thisCond_array,
                            'trialCount': trialCount_array,
                            'contrastRule': contrastRule_array
                            })

# save the csv file + pickle

# CSV file
output_file.to_csv(data_fname, index = False)

   
print('FILE SAVED')

