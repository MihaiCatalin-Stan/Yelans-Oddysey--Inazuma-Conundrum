#### Birladeanu Raluca-Monica 325CA
#### Stan Mihai-Catalin 325CA

# Yelan's Odyssey: Inazuma Conundrum

## Game description
	-> Yelan's Odyssey: Inazuma Conundrum is a game inspired by the popular game Genshin Impact. Even though the characters are not original, the plot of the game and the dialogues sure are. We tried to make immersive dialogues that made the characters feel real, as well as a gameplay that included both a chill story-driven part, and a more unique combat style. 

	-> The story follows Yelan, who is tasked with finding out what is happening in Inazuma. She meets all sorts of characters on her way, and the game is deeper than it first seems to be. Although it is made to be light-hearted and fun, the conversations with Alhaitham and Xiao respectively deal with themes such as insecurity and the fear of imperfection, as well as depression and hopelessness. I strongly believe that while games may be an escape from reality for many, they can also try to bring some sort of comfort with their words. This is why we tried to make the dialogues feel real, and why they were actually thought out to be metaphors for how humans feel in our society. The game is made to be both fun, but also thoughtful and comforting for those who want to pay more attention to the dialogue.

	-> The combat is partly inspired by pokemon - especially the combat with the geo and dendro slimes, since those ones include the basic options such as Flee, Attack, Special and Talk. The combat with the actual characters was thought to be more unique, to offer more insight into the specific characters as well as illustrate their traits better. Each special combat has a well thought objective that will help in the final fight (that is yet to be implemented).

## Combat
The combat that is currently accessible is:

	Xiangling combat - With Xiangling we will have a cook-off and we will have a list of ingredients to pick from. There are three valid recipes, and if the user picks wrong, they will receive damage. If they make the right dish, they will win the combat. The Feed Gouba option allows us to feed Gouba and it also offers a hidden achievement if the user persists. The Advice option makes Xiangling give us some hints about the right recipes.

	Xiao combat - Xiao's combat can be beaten in 2 ways: pacifist and genocide (yes, that was an Undertale reference). We have the Lament and Mercy options which will help Xiao regain his hope. At first he will deal damage to us, which might make the player think sparing him is not the way to go, but when his Emotion grows, he will stop dealing damage. The other options are Fatebound and Banish. Banish acts as an execute and Fatebound isn't actually an ability, it is a way to represent Xiao succumbing to the cruel fate and not trying to change it. The post-combat dialogue is supposed to be a heartwarming way of talking about depression and struggles in life. Even though the game is pretty light-hearted, we are trying to subtly give some hope to the players that might find some solace in our words.

	Nahida combat - In Nahida's combat we can read minds and discover pieces of information, rumors. With those rumors, we can piece together what happened in Inazuma and discover it in a more interesting way. Analyze allows us to select the information, and Conclusion can be used after three pieces of information were picked. Radish is the easter egg, offering another hidden achievement if the player persists with it. 
	Every combat has a pre-combat dialogue and a post-combat dialogue, one that can be accessed if the player interacts with the character after combat. After that, the combat is replayable and the player can replay every combat in order to get the missing achievements.

## Technologies used

	The game is made using pygame, but we also used numpy and scipy.ndimage for the gaussian blur feature (used for achievements).

## Game commands
	The player movement is done with WASD, F is used for interacting with both objects and characters (the player has to colide with them in order to interact), E is for the Achievement tab (Achievements will have their name and description hidden till they are unlocked), C for Character Tab (which displays the stats and the equipped artifacts), I for inventory (the inventory is different depending on the combat we are in. The default inventory is the one that has artifacts and special items in it.).

## Team contribution
	Monica: game idea, basic map layout, classes for: scene, npc, player; main menu, scene transition, npcs, talking option, dialogues, UI, character/achievement/inventory page. Some of the item description are taken directly from the game we got our inspiration from, but the dialogues and achievements are original, some of them making references to other games I enjoyed.

	Mihai: backgrounds (design), characters (design), frames for walk animation, image editing for dialogue pics, inventory pics, combat (with functionalities and necessary derivate classes such as npc_in_combat)

## Problems encountered
	Honestly the biggest struggle was the fact that my initial Python knowledge came from a really short and basic course I took in highschool so i started out with a 4 hour tutorial that really came in handy. The thing I remember most from the video is the guy telling me that Pygame is really good at helping us display images on the screen. And it really is, the game would've been impossible without my colleagues who did the amazing art (Art that is inspired partly by the artist @EkaSetyaNugraha, that I contacted and got permission from to use his character designs as inspiration).

	Another struggle was that the game was really slow at some point, and we had no idea what was wrong with it, since the inventory seemed to be working well till then. We did discover that the problem was that our artifacts were 10kx10k in size, and making the size much smaller solved all the problems. Jumping was also a problem at first, and we did realize how to fix it, but it was too much code to write in order to implement the platforms and some areas would've been unaccessible, so for now Yelan can fly!

## Game impressions
	Overall it was a really fun project that I have many more ideas for that we plan on extending in the future. There are two more upcoming regions packed with content, and we can't wait to build on our knowledge and polish the code in order to make an even better game. There is a lot ahead, and it really brought me a lot of joy to code it and to design the dialogues and the interactions/combats. It was a really fun journey, and we hope you will also enjoy it!

⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⣤⣤⣶⣶⣶⣾⣿⣶⣶⣶⣶⣶⣶⣦⣶⣤⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⣟⡽⣯⢻⡟⣿⣻⣿⣿⡿⣿⣽⢿⡻⣽⣹⡟⣟⢯⣻⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣾⣻⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⢻⠿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣻⣷⡿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣷⣦⠀⠀⠀⠀
⢰⣷⣤⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀
⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀
⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⠹⣟⣛⣭⣤⣦⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀
⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣿⣿⣻⣽⣷⣿⠾⣛⡽⠞⠛⡉⡉⠄⡠⢀⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀
⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⢿⣿⣳⠿⠛⢉⠠⢀⠍⡐⠈⡄⢡⠐⠌⡐⠠⣿⣯⢿⣯⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀
⠀⠀⣷⣿⣿⣿⣿⣿⣿⣻⣾⣿⣻⣿⣈⡉⠄⢂⠡⢂⠂⣁⠂⠤⢓⠒⡓⢛⠲⢖⣳⣿⣯⣿⣞⣿⡷⣿⢯⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀
⠀⠀⣿⣿⣿⣿⢿⣿⣳⣿⣷⣟⣡⣂⣠⡁⠊⠄⠒⡠⠡⠠⠘⡐⢠⣶⣶⣿⣿⣿⣿⣿⡿⣿⣿⣿⣽⢯⣿⣻⣿⢿⣿⣿⣿⣿⣿⣿⡇⠀⠀
⠀⠀⣿⣿⣿⣟⣿⣿⣿⡿⠟⣿⣿⡿⣿⡟⠡⢈⠅⠄⡑⡄⠣⠔⠛⠁⠸⡟⠻⡙⠙⢋⠃⠈⣹⣿⢾⣻⢷⣿⢯⣿⣿⣿⣿⣿⡿⣿⡇⠀⠀
⠀⠀⣿⣿⣻⣿⣾⡿⣿⠀⠀⣏⣀⡥⠷⠞⠀⠃⠈⠁⠀⠀⠀⠀⠀⠀⠉⠉⠉⠙⠛⠛⠒⠂⢸⡿⣯⣿⡿⣞⢯⡿⠛⠻⢿⣯⢿⣽⡇⠀⠀
⠀⠀⣿⣿⢿⣟⡿⣿⢨⠹⡋⠏⠂⠁⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠜⠛⠉⣳⡝⣎⢧⡇⠀⠀⠀⠹⡞⣼⡇⠀⠀
⠀⠀⣿⢿⣻⢞⣿⢸⡇⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡷⢎⡳⢾⣷⠍⠁⠀⣠⢟⡼⣧⠀⠀
⠀⠀⢸⣟⡯⣞⣽⢺⡀⠀⠀⠀⠀⠀⠀⠀⠀⠢⠤⠀⠀⠀⠄⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡟⣭⠳⡟⠋⠀⢀⣸⣾⣏⢶⢻⡀⠀
⠀⠀⢸⣯⣷⢣⢞⣏⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣝⡲⣻⣷⣖⣞⣿⣿⣧⢻⣮⢏⣧⠀
⠀⠀⢸⣿⣿⡘⣎⣿⣿⠷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠠⣂⣴⡟⣦⣽⣿⣿⣿⣿⣿⡟⡖⣿⠈⠻⢼⡆
⠀⠀⠘⣿⣿⡕⣎⢼⣿⠀⢿⣷⣦⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⣠⠖⠋⢹⣿⣿⣿⣿⠇⠂⢿⣿⣿⣿⡿⡹⣼⠇⠀⠀⠀⠀
⠀⠀⠀⣿⣿⡗⣜⢪⣿⣾⣿⠿⠛⠛⠏⢓⠶⠦⢤⡤⣤⣀⣀⣀⣂⡤⠴⡷⠟⠁⠀⠉⠉⠉⠛⣯⠙⣿⠦⣜⣿⣿⢟⡼⣱⠏⠀⠀⠀⠀⠀
⠀⠀⠀⢿⠟⠻⣜⢦⣹⡛⠛⢶⠀⠀⠀⠈⢁⣠⣦⣴⣏⡩⣱⠒⣒⣋⢹⡥⡂⠀⠀⠀⠀⡀⢈⢳⡀⠘⠿⣹⡿⣋⢞⣴⠋⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠈⠀⠀⠈⠛⣶⡇⠀⢣⢠⡖⡇⢠⣥⣾⣯⣴⠋⢻⠀⣿⣿⣿⣿⡖⠉⠑⣴⣦⣤⠁⣤⣼⡇⠀⠘⠛⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢀⣾⣿⡷⠔⡻⣿⡋⠅⣜⣒⠁⠱⣿⣿⣿⣿⡶⠀⠀⠀⠀⢀⡟⠲⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣞⡛⢿⠁⡐⣌⢌⣄⡱⢠⠊⠉⠙⠛⠻⠿⠛⠁⠀⠀⠀⠀⡼⠀⠆⠙⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣟⣴⣩⣟⣤⣇⣿⢠⢮⠁⡇⠀⠤⠀⠀⠀⡀⠀⠀⠀⠀⠀⣴⠁⡐⠈⠄⠈⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⡀⢀⠴⠉⠹⣿⣿⣿⣿⣿⣿⣾⣾⣄⣧⣁⡂⠥⠘⢠⠐⡁⠀⠀⣠⠊⢸⡆⠠⠐⠈⠂⠈⢣⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢠⠊⢹⠁⢀⡀⢀⡽⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣾⣶⡿⠃⢀⢸⣧⠐⠠⢁⡂⠀⣀⡫⠘⣆⣀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢰⠃⠀⠈⣼⣠⡡⢺⠁⢠⣿⣿⣿⣿⡿⣽⣻⠏⠉⣐⣢⣿⣿⣿⣿⣿⡟⠛⠛⢺⠾⡌⣁⣺⡟⠚⠈⠅⠀⠀⢨⠇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣧⠀⠀⢀⠊⠀⠀⡞⠀⣼⣿⣿⣿⣿⣿⣳⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠘⠲⡟⠒⠫⠙⠳⡄⠀⠀⢀⡰⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠙⠓⠒⠛⠷⠖⠊⠀⠀⠈⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠙⢮⣴⡬⠦⠟⠓⠒⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
# Yelan and every one of us wish you an amazing day and very happy Holidays! <3