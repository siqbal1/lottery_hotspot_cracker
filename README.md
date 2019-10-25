# lottery_hotspot_cracker

Project explores a stastical analysis of the psuedo randomness the Hotspot Lottery Game. The hotspot is played as follows:

1. Plays every 4 minutes
2. Number range is [1-80] 
3. 20 numbers out of 80 are selected as winning numbers
4. Each number has a 1/4 probability of being selected
5. Player can select upto 20 numbers and winners are payed out depending on number selected correct

Just to preface this, I did not do this project with any expectation of breaking the lottery for personal gains as a some sort of get rich quick scheme. My family owns a smoke shop, so we have this lotterry game that plays over there. I thought it would be an interesting project to see if I could use my programming knowledge and limited stats knowledge as a way to help people out. also this was a really a nice project to enhance my skills with Python such as: object manipulations, list manipulations, and other problem solving techniques using programming methods.

Firstly, I was not able to use my heuristic function to significantly raise the odds of winning on a single number, but I was able to raise it (however slightly). My heuristic functions on a day to day basis was able to select a single number with a probability of 24% - 30%. So if you were looking to read about a way to crack the lottery this is not the place to be looking. Instead I will discuss the process and methodology to get the increased probability.

In order to make different heuristic functions I had to look at different aspect of the selected numbers.
First I found that 75% percent of the current 20 winning numbers, are selected from the previous draws losing spots
and 25% are selected from the previous draws winning numbers.

Since my goal was to just increase the odds of selecting just a few numbers, i just focussed on just selecting numbers from previous winning numbers. Since 25% of previous numbers are selected on avg, we can expect 5 numbers out of the 20 to win again in the next drawing.

So focussing on just winning numbers we need to find a way to distinguish these numbers and test different aspects of the pseudo random generator.

With some data analysis I was able to find that each number is drawn once every 4 draws (1 selection / 4 draws).

Focussing on the each spots draw distances (the number of draws in between when a spot is selected as a winner):

I found that since on average each number is selected every 4 draws, that if a number has a long previous draw (>= 8), then for the next few draws we can expect the draw distance to be shorter. Though this sounds reasonable enough the cases where this occur are very rare. In my analysis I found that if we take a histogram of the interdraw distances, then the longer (in draws) it takes for a number to be selected the lower the probability is for the number to be selected at that specific draw. 

I found that the histogram of inter draw distances followed a pattern that was similar to an exponential distribution, but with finite values. This comes in handy because we can use some of the properties of the exponential distribution to our advantage. I found that it was we can expect upto 45% of numbers to selected again within 2 draws of being selected. Similarly within 3 draws upto 59% of numbers are selected again.

So using these stats, one of my heuristics takes a look at the current draw distances as well as the avg of the last few draw distances to assign a confidence value on spots.

My next heuristic focussed on the averages of the current winning spots list:

For each draw I calculated the mean of the avg draw list, as well as std_dev, variance, etc...
I found that the mean of the winning spots is centered around 40 with a std_dev of 3.5.
Using this information I tested the following theory. For the current draw if we have a high avg winning spot list (ex: 49),
then for the next draw we can expect to have a winning spot list with a low avg (ex: 33). If there is a high or low avg we can make an assumption that the majority of numbers in the winning set are either >40 or <40. So if I found a winning spot list with a high avg, I would place extra confidence on spots 1-30. Similarly with a low avg, I would place extra confidence on spots 50-80. Testing this observation it does seem to work for a majority of times a case such as that happens. But the problem is the frequency with which we get winning spot list with an avg that deviate from the mean greatly is low.


My next Heuristic focusses on the modes of each day:

In my data analysis I found that, since each number is expected to get selected onces every 4 draws, we can expect each number to win 75 times a day. By analyzing spot counts from day to day, I was able to find that the data does meet the expectations. Most numbers reach a selection count of around 75 within a day, but there are a few outliers. By analyzing the spot histograms of each day I found the 4 least selected spots, and the 4 most selected spots usually varied widely from the expected avg of 75 selections in a day. Using this, information I tested to see if picking from among the top 5 numbers resulted in a higher winning number selection rate. The tests did seem to work out in my favor, showing a slight, but difnitive increase in selection odds. Which is to be expected.


My final worknig Heuristic tries to adapt to the randomness of psuedo number generator:

In my data analysis I found that spots will spontaneosly go on a streak of consecutive selections, this heuristic is menat to 
find numbers that might be going through a low draw streak and put more confidence in that number. I did this by analyzing the avg of the last 3-5 draws of each spot and checking if the avg inter draw distance is lower than 4. If it is, I put more confidence in that spot. This isn't as much based on any sort of statistical method, but much more about embracing the randomness of the pseudo random generator and adapting to it.


I have tried and tested many other heuristics and aspects of the date set, but thse are the ones that have worked best so far. 
I might do further data analysis after further research.






