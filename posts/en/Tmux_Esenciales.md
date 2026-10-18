---
title: Essential things to know about Tmux
date: 2025-11-22
---
# Tmux - Essentials

Tmux is a really good tool for handling different sessions in the terminal and different layouts. You can disconnect from a tmux session and reconnect later, picking up right where you left off. There's a huge amount of things you can configure in tmux, from keys, bars, keybindings, themes... and a bunch of commands that can end up sounding intimidating. Still, knowing just a handful of them, and they're pretty intuitive, can help you deal with your day-to-day in a really easy and useful way. I've been using tmux for over four years and never once dared go past these four basic commands, and even so I've found a whole lot of utility and pleasure in the thing when it's time to work.

## Sessions
If you've never worked with tmux and this is your first time, or you just don't have any active sessions, simply type in the console

```
tmux
```

This opens a new window in a single panel covering the whole screen, or the whole console.

One of the most useful things tmux has is the ability to detach (unlink?) the session we're in right now, and its capacity to reconnect later on, coming back to the point where you left it, with every window and tool you had open at the time.

To detach from the new session you've created simply press ```ctrl``` + ```b``` and then ```d``` (detach). Now you'll be back at your original terminal.

You can see the tmux session you had before, and any you create in the future, with the command:

```
tmux ls
```

And reconnect (attach) to the most recently created session, using:

```
tmux a
```

## Prefix

Let's talk about the prefix. This kind of command is common in a lot of linux tools, vim for example, and they prompt the application in question to sit and wait for a key press before running a command. Instead of doing a key combination, like ```ctrl``` + ```c```, to copy, what we do is press our prefix command to put tmux in a waiting state and then press the key we want to run the order. The default configuration is ```ctrl``` + ```b```, though we can change it to whichever we like (I use ```ctrl``` + ```space```). Every command in a tmux session is started this way. You press the combination first and then the command you want to run. From here on, we'll refer to the prefix command as ```prefix```.

## Windows and panes

When we're using tmux, there are two basic concepts you have to get a grip on if you want to be even remotely productive: windows and panes. You can think of windows as a tab inside a tmux session. A tab like the one you open to get to a different site in firefox, for example. These windows are listed in the bottom bar of tmux. Each window can have multiple panes, which are the ways we have of splitting the screen around the different layouts of the window.

## Windows

Each window has a number predefined to represent it. If we want to move around our windows we can use the prefix plus the number of the window we want to go to, so ```ctrl``` and ```0```, to move to window 0. When you have a lot of windows, getting around them starts to get tedious, so you can rename them with ```prefix``` and ```,```, and give them whatever descriptive name you want.

## Panes

Panes are how you get to split each window; to create them you can use ```prefix``` and ```%```, to make a vertical split between the panes.

To know the number of each pane you can press ```prefix``` and ```q```, the number of each pane will show up on your screen for a few seconds. That way you can navigate between panes, with ```prefix``` and ```q``` and then the number ```1```, to position yourself on the first one, or simply move right to left or top to bottom.

Most of the time it's going to be really useful to zoom into a single pane. Say you're programming and you want to quickly test your app, or launch it in the background. You can open a new pane, launch your app, go back to your programming pane, and ```prefix``` and ```z``` to maximize the pane. The rest of the panes that aren't maximized will sit in the background, so it can come in handy for heaps of applications that need to stay alive.

## Command summary

```tmux``` to create a tmux session
```tmux ls``` to see the tmux sessions currently alive
```tmux a``` to connect to one of your tmux sessions
```ctrl``` and ```b``` as tmux's default prefix command
```prefix``` and ```d``` to disconnect from the tmux session
```prefix``` and ```c``` creates a new window
```prefix``` and ```0 - 9``` to move to the window with that specific number
```prefix``` and ```,``` renames the current window
```prefix``` and ```%``` splits the window in two vertically
```prefix``` and ```"``` splits the current pane in two horizontally
```prefix``` and ```q``` to see the numbers of your panes
```prefix``` and ```q``` ```0 - 9``` to switch to the pane with the corresponding number
```prefix``` and ```z``` to zoom into the pane


This is nothing but the beginning; at some point I'll talk about my hotkeys and how to improve your workflow with just two basic things. The good thing about tmux, like all of linux, is that it's hackable and totally adaptable to your way of working.
