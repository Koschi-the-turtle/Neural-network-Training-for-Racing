# Neural-network-Training-for-Racing
A few months ago I made Kawaii Tank Miniature, a simple top-view racing game. Then, I got the idea of training an AI to race on it. But it was terrible and I encountered an absurd amount of bugs which made me give up for a while. Then I decided to use Claude to fix most of these bugs, and I watched some tutorials to better understand what the hell I was suppose to do. And it finally worked, so after a lot of tweaks, I was finally able to make the AI complete a full clean lap.

https://github.com/user-attachments/assets/0f04076d-8cb4-41d1-a37f-54059ed19864

# How it works

This is a generational algorithm, meaning it first spawns multiple tanks (population), and let them run, it then takes the one with the best fitness (calculated based on a lot of factors) and spawns a new generation of tanks based on that one's run, but with a certain amount of changes (mutation), it then takes the best tank of that generation and use it for the next, and it does the same thing for x generations.

Therefore, at the end, you get the best simulation of all runs, which is then simulated visually for you.

The AI tank has access to acceleration, direction and braking. It uses raycasts which tells it how far from the walls it is in 7 directions. Using those datas, it can tell when to turn, accelerate or brake, because it "sees" whether there is a straight line or whether a corner is coming up, though it's not perfect, which explains why you need a generational algorithm to end up with an actual clean lap. However the AI behaves like electricity, meaning it always tries to reach its objective in the easiest way possible, which leads to it "cheating" its way around, so you have to do a lot of tests and apply constraints so that it does what it was intended to do.

# How to use

Simply download the zip file, and execute the .exe file in it. On the menu, you can use your keyboard's arrows to choose the tank you want, then you can either press enter to play like you normally would, or preferably press T, to start the AI's training. It trains on 30 generations, which takes a few minutes for me, but I guess it depends on your pc's capabilities. Sometimes, it looks like the program is taking a lot of time on a generation, that's normal, the window simply didn't refresh correctly and doesn't always show the current generation. Just put the window in the background and do something else idk, then when you come back to it it should have refreshed to the actual generation. Either way, it's not that big of an issue, just wait for it to finish, and then it will simulate the final run for you. 

NOTICE: It might not always manage to complete a full lap, you can predict it if you see that the best fitness didn't get over like 15 or 20k, you can always just re-run the program.
