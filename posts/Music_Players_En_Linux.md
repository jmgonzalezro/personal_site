---
title: Music Players en Linux
date: 2026-02-05
---
# El estado de los reproductores de música en Linux en el 2026

Si todavía no lo sabes, todo el mundo está deshaciéndose de [microslop](https://www.windowscentral.com/artificial-intelligence/microslop-trends-on-social-media-backlash-to-microsofts-on-going-ai-obsession-continues) para empezar a usar sistemas que realmente respetan quién eres y los gustos que tienes. También, al parecer, hay mucha gente que está empezando a quitarse la suscripción de [spotify, que no deja de subir](https://www.theverge.com/news/862465/spotify-premium-us-price-increase-2026), para apropiarse de los medios tanto musicales como visuales que se me consumen a diario.

Este tipo de modas parecen retomar ciertas costumbres que de vez en cuando se van viendo en internet, que parece que tienen una gran aceptación y que pueden llegar a ser algo más de lo que parece, pero se quedan en agua de borrajas y nada más que encaja con ciertos grupos de usuarios "avanzados", o más bien... personas que no se contentan con cualquier cosa y no les importa profundizar en un tema hasta que obtienen lo que quieren. Para que todos nos entendamos... frikardos. Esperemos que en esta ocasión y con la cantidad de gente que se está dando cuenta de que tienes que tener un verdadero ecosistema para ver todas las series o películas que quieres y escuchar toda la música que te apetece, teniendo que pagar grandes cantidades y que cada vez es más insostenible, no se quede en esos medios caminos que nunca llegan.

Espero que no pase como con modas que intentaron volver, ya sean las cintas o los cassette, y que se queden en forma de usar torrents una vez más y transferirnos la música entre nosotros de manera más educativa, ilustrativa y mucho más entretenida, que no tener un algoritmo manipulado poniéndote lo que quiere.

Llegados a este punto, realmente creo que los artistas ganarían más dinero con aquello de "sube mis flows a internet" que estando a espensas de que el algoritmo, totalmente manipulado por grandes discográficas y por spotify que lo único que le interesa es sacar más dinero, te favorezca el día adecuado en el momento oportuno. Por lo menos, cuando busco los artistas que me gustan en [soulseek](https://www.slsknet.org/news/), no me devuelven cientos de artistas creados por inteligencia artificial que suenan igual y que distraen la atención de lo que busco. Aunque en ocasiones, hacen bastante gracia, como aquella vez que sacaron a "Taylow Swong" en QTEM. Y con todo esto hay que recordar que cuando compras el disco, estás dándole más dinero al artista que con miles de escuchas del mismo disco en las plataformas online. Y yo, personalmente, escucho muy pocos discos cientos de veces, pero sí me gustaría tenerlos en mi colección.

En este aspecto, ciertos artistas que sigo todavía siguen sacando sus discos en [bandcamp](https://bandcamp.com/) y puedes comprar el disco y algo de merchandising. Otros tantos artistas, como [Erik Urano](https://erikurano.com/) se han pasado de Tidal, que teóricamente no te quita tanto dinero como el resto. Aunque, [viniendo de quien viene](https://es.wikipedia.org/wiki/Jay-Z), no dudo en que sea igual o peor. El tiempo dirá.

![Erik Urano](https://www.sala-apolo.com/uploads/media/default/0001/07/thumb_6492_default_wide.jpeg)

Claro que, ya no vivimos en la edad de piedra, y todos queremos llevar con nosotros nuestra música a todas partes. El estar cargando y descargando música en el móvil puede ser divertido al principio, pero cuando se transforma en una tarea, es algo tedioso y puedes llegar a pensar que te vuelves a tu suscripción de spotify o youtube music, y estaría totalmente justificado. Sin embargo, y sin haberlas probado, hay soluciones para poder llevar tu música a todas partes siempre y cuando en casa tengas una conexión a internet. Pues esta tecnología del futuro que te permite stremear FLAC, ha spotify le ha llevado 2 décadas en desarrollarla, y a otros le ha llevado un proyecto de fin de semana en sacarlo. Estos proyectos son [JellyFin](https://jellyfin.org/) y [Navidrome](https://www.navidrome.org/). Ambos gratuitos y de código aabierto.

Esto quizá haga que escuchar música sea hobby de coleccionista, como lo fue hace unos años. Y poder ver que la música que has escuchado sigue ahí, y te mira, y puedes ver la portada, y no es un intento constante de buscar la canción o el disco que quieres escuchar pero que no te acuerdas como se llama pero que sabes que lo encontraste dentro de tal género o lista predeterminada.

Una vez echada la brasa sobre la política de la sociedad de las suscripciones y antes de volverme en un hermitaño en una cabaña con un portátil y una distro de linux de bajo consumo y sin software más que un terminal... voy a comentar algunos programas y aplicaciones que hay para escuchar música (y solo escuchar música), en linux y sus difernetes formatos.

_____

A lo que vamos. Hay ciertos reproductores de música que están usándose con diferentes formas y sabores, ya sea integrados en tu escritorio o en formato de aplicación normal y corriente. Algunos más extensibles que otros y todos centrados en hacer una cosa y hacerla bien: Reproducir música.

## Amberol
Amberol es uno de esos reproductores sencillos que no quieren ser más de lo que aparentan. Se integra con GNOME y es mínimo, pero en el buen sentido. No tiene manejo de librerías, lo que quizá para algunos forme parte del tedio, pero si tienes tus librerías en carpetas está genial. Quizá para usarlo para escuchar música de manera casual o tenerlo como reproductor por defecto, sin complicaciones, es lo suyo.

![Amberol](https://gitlab.gnome.org/World/amberol/-/raw/main/data/screenshots/amberol-full.png)

## Plattenalbum
[Este reproductor](https://github.com/SoongNoonien/plattenalbum) es de esos que me gustaría que me gustase. Está centrado en que tengas tu propio MPD (music server daemon) y con eso hagas todo. No tiene manejo de listas y vas a tener que traerte tu propio MPD. Que a priori no tiene por qué ser complicado, pero ya es una puerta más que tienes que abrir.

Es muy simmilar, funcionalmente, a Amberol, pero en este caso le han puesto una capa para el buscador de música dentro de tu librería. Muy centrado en escuchar música y mientras miras una portada gigante. Aunque sin tener cosas sencillas como ver todos los discos que tienes en tu librería, es algo que no me termina de convencer para que sea más que un reproductor casual. Y a este reproductor casual le tienes que montar el MPD por encima y... bueno.

![Plattenalbum](https://crescentro.se/posts/linux-music-players-2026/plattenalbum.png)

## Tauon

No estoy del todo convencido de querer que toda mi música sea una playlist, pero [Tauon](https://github.com/Taiko2k/Tauon) es lo que intenta. Soy más de poner un disco al completo y dejar que finalice, o poner en aleatorio la música, o poner una radio del género.

Por todo lo demás, Tauon es agradable, fácil de manejar, el sistema de colores es elegante y la manera que tiene de presentarte las carátulas es bastante protagonista. Digamos que es lo que hace foobar20000 sin aquellos complementos raros que la gente personaliza. Si te gustó foobar, te gustará Tauon.

![Tauon](https://user-images.githubusercontent.com/17271572/56716255-f03ba080-678d-11e9-880f-49d6cbf77e60.jpg)

## Conclusión

Hay muchos que se me quedan en el tintero, como [Strawberry](https://www.strawberrymusicplayer.org/), [Clementine](https://www.clementine-player.org/) o [Amarok](https://amarok.kde.org/), que han sido el reproductor de linux de facto por mucho tiempo. Creo que hoy en día tienen un estilo bastante 2010, y aunque no es algo que te haga daño, quizá un pequeño rework sin tanto brillo o transparencia les haría un favor. Son relativamente fáciles de usar y puedes tener tanto listas como librerías.

Pero, en cualquier caso, si quieres usar música en formato mp3 o FLAC o cualquier otro que en ese momento te plazca, todavía tienes opciones, relativamente modernas que pueden servirte tanto si te gusta hacer listas, o si prefieres manejar la librería e incluso si prefieres montarte todo un daemon de sonido desde abajo. La decisión es tuya y creo que ahora mismo se disfruta de una buena salud en cuanto a reproductores y manejabilidad de los mismos.

