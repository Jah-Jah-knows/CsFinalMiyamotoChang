###Cs Final Project Jonah Chang and Wyatt Miyamoto BatterUp! Whitman Baseball
'''
Used streamlit.io for information on formatting and syntax within the library
Consulted chatGPT for basic examples to build off of as well as for debugging help
Would also like to credit our teammates and Coach Jordan Hara for their videos and 
input on earlier versions of the game. 
'''
#Import libraries and dictionaries
import random
import streamlit as st
import PlayerInfo
import string
import pandas as pd

#define remove punctuation function
def removePunctuation(text):
	'''
	Removes punctuation from a given piece of text
	pre-conditions: piece of text
	post-conditions: none
	'''
	newText = ""
	for character in text:
		if character not in string.punctuation:
			newText += character
	return newText

# define function for play again
def resetGame():
	'''
	Resets game to original conditions and generates a new secret name
	pre-conditions: none
	post-conditions: game state that has no previous user interaction 
	and has a new name to guess 
	'''
	st.session_state.game_over = False
	st.session_state.guessInput = "" 
	st.session_state.secretName = st.session_state.remaining.pop()
	st.session_state.tries = 0
	st.session_state.guessHistory = []

#define make rows function
def makeRows(guess, target):
	'''
	creates rows of values to be used in the grid that displays previous guesses
	pre-conditions: a list of keys that correspond to values in the dictionary,
	a guess inputted by the player and a target player to compare the guess to.
	post-conditions: returns a row that shows whether or not the guess was correct and if 
	it is incorrect whether the true value is higher or lower. 
	'''
	row = {}
	for key in ["Name"]:
		row[key] = f"{guess[key]}"
	for key in [ "Class", "Position", "State/Prov",]:
			if guess[key] == target[key]:
				row[key] = f"{guess[key]} 🟩"
			else:
				row[key] = f"{guess[key]} ⬜"
	for key in ["Height"]:
		if int(removePunctuation(guess[key])) < int(removePunctuation(target[key])):
			row[key]= f"{guess[key]} ⬆️"
		elif int(removePunctuation(guess[key])) == int(removePunctuation(target[key])):
			row[key] = f"{guess[key]} 🟩"
		else:
			row[key] = f"{guess[key]} ⬇️"
	for key in ["#"]:
		if int(guess[key]) < int(target[key]):
			row[key] = f"{guess[key]} ⬆️"
		elif int(guess[key]) == int(target[key]):
			row[key] = f"{guess[key]} 🟩"
		else:
			row[key] = f"{guess[key]} ⬇️"
	return row
# main code

def main():	
	#put title on screen.
	st.markdown("<h1 style='text-align: center; color: #26A3FF;'>Batter Up!</h1>", unsafe_allow_html=True)
	st.markdown("<h2 style='text-align: center; color: #FFDE00;'>Whitman Baseball Edition</h2>", unsafe_allow_html=True)
	video_placeholder = st.empty()
	#Create and shuffle list of player names
	if "remaining" not in st.session_state:
		st.session_state.remaining = list(PlayerInfo.playerDict.keys())
		random.shuffle(st.session_state.remaining)
	
	#when all players are used up, create and shuffle again
	if len(st.session_state.remaining) == 0:
		st.session_state.remaining = list(PlayerInfo.playerDict.keys())
		random.shuffle(st.session_state.remaining)
			
	#Get random player
	if "secretName" not in st.session_state:
  	  st.session_state.secretName = st.session_state.remaining.pop()
	secretName =  st.session_state.secretName
	target = PlayerInfo.playerDict[secretName]
	
	#Find videos in dictionary
	targetVideo = PlayerInfo.playerDict[secretName]["silVideo"]
	winVideo = PlayerInfo.playerDict[secretName]["Video"]
	
	#Create path for videos in folder Swings
	targetVideo_path = f"Swings/{targetVideo}" 
	winVideo_path = f"Swings/{winVideo}"
	
	#Initialize game state
	if "game_over" not in st.session_state:
		st.session_state.game_over = False
	if "guessInput" not in st.session_state:
		st.session_state.guessInput = "" 
	if "tries" not in st.session_state:
		st.session_state.tries = 0
	if "guessHistory" not in st.session_state:
		st.session_state.guessHistory = []

	#get user input
	inputText = st.empty()
	guessName = inputText.selectbox("Guess the swing: ", 
	PlayerInfo.playerDict, index = None, placeholder = "Type or select a player..."
	, key = "guessInput")
	
	#If user loses
	# If game is over (Lose or Win), show the final video and stop
	if st.session_state.game_over:
		st.write(f"The Hitter was {secretName}")
		video_placeholder.video(winVideo_path, autoplay = True, muted = True, loop = True)
		inputText.empty()
		
	# If game is NOT over, show the silhouette and check the guess
	else:
		# Check if a guess was made
		if guessName and guessName != secretName and guessName in PlayerInfo.playerDict:
			st.session_state.tries += 1
			st.write(f"{guessName} is not the right hitter")
		
		# Check for loss *after* incrementing tries
		if st.session_state.tries >= 5 and guessName != secretName:
			st.session_state.game_over = True
			# NOTE: The video will display in the 'if st.session_state.game_over:' block above on the next run.
		
		# Show the current silhouette
		if not st.session_state.game_over:
			video_placeholder.video(targetVideo_path, autoplay = True, muted = True, loop = True)
			
		# Check for win (only runs if game is NOT over, but needs to be placed carefully)
		if guessName == secretName and guessName is not None:
			st.session_state.tries += 1
			st.session_state.game_over = True
			st.write("You Win! The hitter is " + str(secretName))
			st.write("You got it in " + str(st.session_state.tries) + " tries")
			inputText.empty()

	# If game is over prompt for play again
	if st.session_state.game_over:
		st.button("Play Again", on_click = resetGame)
	
	#On guess, create table with guess history
	if guessName:
		if guessName in PlayerInfo.playerDict:
			st.subheader("Your Guesses")
			st.session_state.guessHistory.append(makeRows(PlayerInfo.playerDict[guessName], target))
			numbers = pd.DataFrame(st.session_state.guessHistory)
			numbers.index = range(1, len(numbers.index) + 1)
			st.dataframe(numbers)


main()	



