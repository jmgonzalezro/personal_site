---
title: Music Players on Linux
date: 2026-02-05
---
# The state of music players on Linux in 2026

If you didn't know yet, everyone is getting rid of [microslop](https://www.windowscentral.com/artificial-intelligence/microslop-trends-on-social-media-backlash-to-microsofts-on-going-ai-obsession-continues) to start using systems that actually respect who you are and the tastes you have. Also, apparently, there's a lot of people starting to drop their [spotify subscription, which keeps going up](https://www.theverge.com/news/862465/spotify-premium-us-price-increase-2026), to take back ownership of the musical and visual media that gets consumed on a daily basis.

These fashions seem to pick up certain habits that show up on the internet from time to time, which look like they've got huge acceptance and could turn out to be something more than they seem, but they fizzle out into nothing and only ever fit certain groups of "advanced" users, or rather... people who aren't satisfied with anything and don't mind digging into a subject until they get what they want. So we all understand each other... geeks. Let's hope that this time, and with the amount of people realising that you have to have a real ecosystem to watch every series or film you want and listen to all the music you feel like, having to pay large amounts and it being more unsustainable by the day, it doesn't end up in those halfway paths that never arrive.

I hope it doesn't turn out like the fashions that tried to come back, be they tapes or cassettes, and that it stays in the form of using torrents once more and passing music between us in a much more educational, illustrative and far more entertaining way, rather than having a manipulated algorithm putting on whatever it wants.

At this point, I really believe artists would make more money with that whole "upload my flows to the internet" thing than being at the mercy of the algorithm — totally manipulated by the big labels and by spotify, whose only interest is making more money — favouring you on the right day at the right moment. At least, when I look up the artists I like on [soulseek](https://www.slsknet.org/news/), it doesn't hand me back hundreds of AI-created artists that all sound the same and distract from what I'm looking for. Although sometimes they're pretty funny, like the time they put out "Taylow Swong" on QTEM. And with all this we have to remember that when you buy the record, you're giving the artist more money than thousands of listens of that same record on the online platforms. And me, personally, I listen to very few records hundreds of times, but I would like to have them in my collection.

In this respect, certain artists I follow still put out their records on [bandcamp](https://bandcamp.com/) and you can buy the record and some merch. Plenty of other artists, like [Erik Urano](https://erikurano.com/), have moved over to Tidal, which theoretically doesn't take as much money from you as the rest. Although, [coming from who it comes from](https://es.wikipedia.org/wiki/Jay-Z), I have no doubt it's just as bad or worse. Time will tell.

![Erik Urano](https://www.sala-apolo.com/uploads/media/default/0001/07/thumb_6492_default_wide.jpeg)

Of course, we don't live in the stone age anymore, and we all want to carry our music everywhere with us. Loading and unloading music onto your phone can be fun at first, but when it turns into a task it gets pretty tedious and you can end up thinking about going back to your spotify or youtube music subscription, and you'd be totally justified. However, and without having tried them, there are solutions for being able to carry your music everywhere as long as you have an internet connection at home. Because this future technology that lets you stream FLAC took spotify 2 decades to develop, and to others it took a weekend project to ship. These projects are [JellyFin](https://jellyfin.org/) and [Navidrome](https://www.navidrome.org/). Both free and open source.

This might perhaps make listening to music a collector's hobby, the way it was a few years ago. And being able to see that the music you've listened to is still there, and looks back at you, and you can see the cover, instead of a constant attempt at finding the song or the record you want to listen to but can't remember what it's called, yet you know you found it inside such and such genre or default list.

Once I've thrown my two cents on the subscription society's politics and before I turn into a hermit in a cabin with a laptop and a low consumption linux distro and nothing but a terminal for software... I'm going to go through some programs and applications there are for listening to music (and only listening to music), on linux and its different formats.

_____

To the point. There are certain music players being used in different shapes and flavours, whether integrated into your desktop or as a plain old application. Some more extensible than others and all focused on doing one thing and doing it well: playing music.

## Amberol
Amberol is one of those simple players that don't want to be more than they look. It integrates with GNOME and it's minimal, but in the good sense. It has no library management, which perhaps for some forms part of the tedium, but if you have your libraries in folders it's great. Maybe for using it to listen to music casually or having it as a default player, without complications, it's the one.

![Amberol](https://gitlab.gnome.org/World/amberol/-/raw/main/data/screenshots/amberol-full.png)

## Plattenalbum
[This player](https://github.com/SoongNoonien/plattenalbum) is one of those I wish I liked. It's centred on you having your own MPD (music server daemon) and doing everything with that. It has no playlist management and you're going to have to bring your own MPD. Which a priori doesn't have to be complicated, but it's one more door you have to open.

It's very similar, functionally, to Amberol, except in this case they've put a layer on top for the music search inside your library. Very focused on listening to music while you stare at a giant cover. Although without having simple things like seeing all the records you have in your library, it's something that doesn't quite convince me for it to be more than a casual player. And on top of this casual player you have to set up the MPD and... well.

![Plattenalbum](https://crescentro.se/posts/linux-music-players-2026/plattenalbum.png)

## Tauon

I'm not entirely convinced about wanting all my music to be a playlist, but [Tauon](https://github.com/Taiko2k/Tauon) is what tries to do it. I'm more of putting a whole record on and letting it finish, or putting the music on shuffle, or putting on a genre radio.

For everything else, Tauon is pleasant, easy to handle, the colour system is elegant and the way it presents the covers to you is pretty much the protagonist. Let's say it's what foobar2000 does without those weird add-ons that people customise. If you liked foobar, you'll like Tauon.

![Tauon](https://user-images.githubusercontent.com/17271572/56716255-f03ba080-678d-11e9-880f-49d6cbf77e60.jpg)

## Conclusion

There are many that get left on my inkwell, like [Strawberry](https://www.strawberrymusicplayer.org/), [Clementine](https://www.clementine-player.org/) or [Amarok](https://amarok.kde.org/), which have been the de facto linux player for a long time. I think these days they have a pretty 2010 style, and although it's not something that does you any harm, maybe a small rework without so much shine or transparency would do them a favour. They're relatively easy to use and you can have both playlists and libraries.

But, in any case, if you want to use music in mp3 or FLAC format or any other that takes your fancy at that moment, you still have options, relatively modern ones that can serve you whether you like making playlists, or you prefer handling the library, or even if you prefer to set up a whole sound daemon from the ground up. The decision is yours and I think that right now we're enjoying good health when it comes to players and how manageable they are.
