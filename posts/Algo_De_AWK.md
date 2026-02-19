# Por qué deberías aprender un poco de AWK

![AWK y linux se llevan bien](https://opensource.com/sites/default/files/lead-images/linux-penguin.png)


Hace tiempo vi una persona que, en un vídeo, manipulaba el texto de diferentes archivos en cuestión de segundos y me voló la cabeza. Inmediatamente, me puse a buscar como un poseso qué era esa magia que había hecho esa persona y cómo podía aprenderla.

Hasta el día de hoy, el 99% de las personas con las que he hablado y que se dedican al mundo del software no lo han usado nunca. Conocer un poco de sintaxis de AWK, que puede tomarte unos cuantos minutos (o menos aún si usas el chatbot gipiti) aumentaría drásticamente la capacidad de manipular rápidamente los datos de un archivo de texto. Y encima de manera automatizada, evitando errores humanos. Algunas de las cosas más útiles que he utilizado de este pequeño lenguaje, que no son exáctamente "fundamentals", las voy a ir comentando y quizá expandiendo en un futuro.

AWK es un lenguaje de programación divertido. Está diseñado para procesar cadenas de entrada. Una vez en un curso presencial que hice en Telefónica (el cual dejé a medias porque no era para mí...) alguien nos pidió realizar un ejercicio para generar de manera automática talonarios o diferentes tipos de facturaciones para clientes, y que podíamos usar cualquier tipo de lenguaje. Para mí fue bastante gratificante hacerlo en AWK, y encima el código era bastante pequeño en longitud, por sorpresa para todos. Incluso había gente con python haciendo bucles anidados de manera infinita, cuando en AWK me llevó unas cuantas líneas y con lógica muy sencilla.

Para poner unos ejemplos normales, supogamos que tenemos un pequeño archivo de logs.txt que se parece al texto que tenemos abajo.

```07.46.199.184 [28/Sep/2010:04:08:20] "GET /robots.txt HTTP/1.1" 200 0 "msnbot"```

```123.125.71.19 [28/Sep/2010:04:20:11] "GET / HTTP/1.1" 304 - "Baiduspider"```

Estos son solo dos registros generados por apache, algo simplificados, para que la spider de google o los bots de bing no se flipen demasiado con mi web...

AWK funciona como cualquier otra herramienta, como por ejemplo grep, en la consola. Se lee desde stdin y escribe stdout. Es fácil canalizar cosas dentro y fuera de ella. La sintaxis de la línea de comandos que te importa es solo el comando ```awk``` seguido de una cadena que contiene tu programa.

```
awk '{print $0}'
```

La mayoría de los programas de AWK empiezan con un "{" y terminan con un "}". Todo lo que hay entre medias de las doas llaves se ejecuta una vez por cada línea del archivo de entrada. La mayoría de los programas de AWK imprimirán algo. El programa anterior imprimirá por pantalla una línea completa, y print apenda una nueva línea. $0 es la línea completa. Así que este programa es una [operación de identidad](https://en.wikipedia.org/wiki/Identity_function), la cual copia la entrada a la salida sin cambiarla.

AWK parsea la línea de manera automática, utlizando cualquier espacio en blanco como delimitador, fusionando delimitadores consecutivos... Y todo ello está disponible en las variables $1, $2, $3, etc...


```
echo 'esto es una prueba' | awk '{print $3}' // prints 'a'
awk '{print $1}' logs.txt
```

```$ 07.46.199.184```

```$ 23.125.71.19```

Por ahora sencillo, no? Y útil (creo). Cuando necesito imprimir al final del string, la variable especial NF contiene el número de campos en la línea actual. Puedo imprimir el último campo printeando el campo $NF o puedo manipular el valor para identificar el campo basándome en su última posición. O, si quiero, puedo imprimir varias cosas a la vez con el mismo comando ```print```.

```
echo 'esto es una prueba' | awk '{print $ NF}' // prints "test"
awk '{print $1, $(NF -2) }' logs.txt
```

```07.46.199.184 200```

```123.125.71.19 304```

Sigamos avanzando... Quizá te empieza a sonar el tema... pero se pueden quitar las cosas de las que no estamos interesados para printear por pantalla aquellas en las que queremos hacer foco.Otra variable genial es ```NR```, que la podemos usar para formatear la salida del comando ```print```, dejando la coma fuera y sin epsacios, dado que no me interesan.

```awk '{print NR ") " $1 " -> " $(NF-2)}' logs.txt```

```1) 07.46.199.184 -> 200```

```2) 123.125.71.19 -> 304```

Es potente... aunque seguirás pensando que es un poco chorrada. No? Por cierto, hay una función adicional que es ```printf``` que funciona de la manera que esperas, en caso de que prefieras más opciones de formateo. Ahora, no todos los archivos están separados con espacios en blanco o no todos los string. Te estoy mirando a tí, fechas...

```
$ awk '{print $2}' lgos.txt
```

```[28/Sep/2010:04:08:20]```

```[28/Sep/2010:04:20:11]```

El campo de fecha está separado por "/" y ":". Pero creo que voy a centrarme en hacer piping que en aprender la sintaxis de AWK, porque así se le ve más sentido, y ya cada uno que se las apañe con lo de buscar nuevas formas de hacer las cosas con AWK. Lo que voy a hacer a continuación es usar una "pipe" de la salida del comando anterior y meterle a otro AWK el comando para que lo separe a partir de los dos puntos. Para ell, el segundo programa tendrá que tener su propio {}. Tampcoo quiero entrar en lo que significa, simplemente mostrar cómo se separarían las cosas.

```
$ awk '{print $2}' logs.txt | awk 'BEGIN{FS=":"}{print $1}'
```

```[28/Sep/2010```

```[28/Sep/2010```

Simplemente he especificado que quiero otro ```FS``` (field separator), y que quería imprimir el primer campo. Similar a cómo se haría el manejo de strings en otros lenguajes. ¿Y para quitar el carácter, ese [ que existe antes de la fecha?

```
$ awk '{print $2}' logs.txt | awk 'BEGIN{FS=":"}{print $1}' | sed 's/\[//'
```

```28/Sep/2010```

```28/Sep/2010```

Podríamos seguir dividiendo el string en ls diferentes "/" que contiene y coger el  objeto que queramos accediendo a través de su posición con el mismo truco, pero creo que llegados a este punto, lo entendemos. Ahora, aprendamos un poco de lógica. Si solo quiero devolver las primeras 200 líneas podría usar ```grep``` pero terminaría con la dirección ip que contiene 200, o una fecha del año 2000. Podría obtener el primer campo que tiene un 200 con AWK y entonces usar grep, pero entonces perdería toda la línea, su contexto. AWK soporta bucles "if" sencillos. Como por ejemplo...

```
$ awk '{if ($(NF-2) == "200") {print $0}}' logs.txt
```

```07.46.199.184 [28/Sep/2010:04:08:20] "GET /robots.txt HTTP/1.1" 200 0 "msnbot"

Ya lo tenemos. Así podríamos tener todas las líneas que tuviesen en su "status" un 200. El if debería ser familiar a estas alturas de la lectura (porque sino... estarás flipando) y creo que no requiere explicación.

Terminemos ahora con un ejemplo estúpido de cómo el código de AWK mantiene un estatuso en múltiples líneas. Supongamos que quiero sumar todos los campos de estatus del archivo (que te puede venir al pelo para solucionar los adventofcode o sacarte de un apuro en el trabajo). Hay ejemplos como este bastante obvios, pero uno que uso yo a menudo es capturar el tamaño de los archivos generados y de todos los artefactos de un proceso de Machine Learning y printearlos en el logger. Puedo saber el tamaño de los archivos generados y la ram que voy a necesitar solo con un compando sencillo de AWK.

```
$ awk '{a+=$(NF-2); print "Total so far:", a}' logs.txt
```

```Total so far: 200```

```Total so far: 504```

Suele interesarme más el valor final que la acumulación de los mismos. Y puedo hacerlo con comandos conocidos en el mundo de linux o la programación como ```tail -n1```, que printeará la suma después de que el proceso haya finalizado, usando el END para ello.

```
$ awk '{a+=$(NF-2)}END{print "Total:", a}' logs.txt
```

```Total: 504```

Creo que ha quedado más o menos claro el poder de AWK y cuándo usarlo. Para cuestiones sencillas de manipulación de archivos de texto, conociendo dichos archivos, es bastante útil y si lo haces cuando estás con más personas, el efecto wow está asegurado. La única pega es que a veces es algo diferente a la manera de programar, aunque tiene muchas similitudes a comandos de linux normales, y entendiendo los diferentes tipos de encapsulados de código y las posiciones, se pueden hacer cosas realmente sencillas y rápidas.

Espero que haya sido útil, o al menos haya sido una lectura entretenida.