# Tmux - Esenciales

Tmux es una muy buena herramienta para manejar diferentes sesiones en la terminal y diferentes diseños. Puedes desconectarte de una sesión de Tmux y volverte a conectar más tarde y seguir donde lo habías dejado. Hay una gran cantidad de cosas que puedes configurar en tmux, desde teclas, barras, atajos, temas... y un montón de comandos que pueden llegar a sonar intimidantes. Sin embargo, con solo saber un puñado de ellos, que son bastante intuitivos, te pueden ayudar a lidiar con el día a día de una forma muy fácil y útil. Llevo usando Tmux por más de 4 años y nunca me había aventurado a pasar más allá de estos cuatro comandos básicos, y aun así he encontrado en la herramienta un montón de utilidad y placer a la hora de trabajar.

## Sessions
Si nunca has trabajado con tmux y esta es tu primera vez o si no tienes sesiones activas, simplemente escribe en la consola

```
tmux
```

Esto abrirá una nueva ventana en un solo panel que cubrirá toda la pantalla, o la consola entera.

Uno de las cosas más útiles que tiene tmux es la función de hacer detach (desligar?) la sesión en la que estamos ahora mismo y su capacidad de volver a conectar más adelante, volviendo al punto donde lo habías dejado, con todas las ventanas y herramientas que tenías abiertas en su momento.

Para hacer detach de la nueva sesión que has creado simplemente presiona ```ctrl``` + ```b``` y después ```d``` (detach). Ahora habrás vuelto a tu terminal inicial.

Puedes ver la sesión de tmux que tenías antes, y todas aquellas que crees en un futuro, con el comando:

```
tmux ls
```

Y reconectarte (atach) a la última sesión creada, usando:

```
tmux a
```

## Prefix

Hablemos del prefix. Este tipo de comandos son comunes en muchos tipos de herramientas de linux, como por ejemplo vim, y elicitan que la aplicación en cuestión quede a la espera de que se presione una tecla para ejecutar un comando. En vez de hacer una combinación de teclas, como ```ctrl``` + ```c```, para copiar, lo que hacemos es presionar nuestro comando prefijo para posicionar a tmux en espera y después presionar la tecla que queremos para ejecutar la orden. La configuración por defecto es ```ctrl``` + ```b```, sin embargo la podemos cambiar a cualquiera que queramos (yo uso ```ctrl``` + ```space```). Todos los comandos de una sesión de tmux son iniciados de esta forma. Presionas la combinación primero y después el comando que quieras correr. A partir de ahora, nos referiremos al comando ded prefix como ```prefix```.

## Ventanas y paneles (windows and panes)

Cuando estamos usando tmux, hay dos tipos de conceptos básicos que has de controlar si quieres ser medianamente productivo: windows y panes. Puedes pensar en windows como una pestaña dentro de una sesión de tmux. Una pestaña como la que abres para entrar en una web diferente en firefox, por ejemplo. Estas windows están listadas en la barra inferior de tmux. Cada window puede tener múltiples panes, que son las maneras que tenemos de dividir la pantalla en torno a los diferentes layouts de la widnow.

## Windows

Cada ventana tiene predefinido un número que las representa. Si queremos movernos en torno a nuestras ventanas podemos usar el prefix más el número de la ventana donde queramos movernos, de tal forma ```ctrl``` y ```0```, para movernos a la ventana 0. Cuando tienes muchas ventanas se empieza a hacer tedioso manejarse entre ellas, por lo tanto las puedes renombarar con ```prefix``` y ```,```, y poner el nombre descriptivo que quieras.

## Panes

Los paneles es la manera que tienes de dividir cada ventana, para crearlos puedes usar el ```prefix``` y ```%```, para hacer una separación vertical entre los paneles.

Para saber el número de cada panel puedes presionar ```prefix``` y ```q```, aparecerá el número de cada panel en tu pantalla durante unos segundos. Así puedes navegar entre los paneles, con ```prefix``` y ```q``` y luego el número ```1```, para posicionarte en la primera, o simplemente moverte de derecha a izquierda o arriba a abajo.

La mayoría del tiempo va a ser muy útil hacer zoom en un solo panel. Por ejemplo, estás programando y quieres testear rápidamente tu aplicación, o lanzarla en segundo plano. Puedes abrirte un panel nuevo, lanzar tu aplicación, volver a tu panel de programación y ```prefix``` y ```z``` para maximizar el panel. El resto de paneles que no están maximizados estarán en segundo plano, por lo tanto te puede servir para montones de aplicaciones que necesiten estar vivas.

## Resumen de comandos

```tmux``` para crear una sesion de tmux
```tmux ls``` para poder visualizar las sesiones vivas de tmux
```tmux a``` para conectarte a una de las sesiones de tmux
```ctrl``` y ```b``` como comando prefix por defecto en tmux
```prefix``` y ```d``` para desconectar la sesion de tmux
```prefix``` y ```c``` crea una nueva ventana
```prefix``` y ```0 - 9``` para pasar a una ventana con el número concreto
```prefix``` y ```,``` renombra la ventana actual
```prefix``` y ```%``` divide la ventana en dos de manera vertical
```prefix``` y ```"``` divide el panel actual en dos horizontales
```prefix``` y ```q``` ver los números de tus paneles
```prefix``` y ```q``` ```0 - 9``` cambiarte al panel con el número correspondiente
```prefix``` y ```z``` hacer zoom en el panel


Esto no es más que el principio, en un futuro hablaré de mis hotkeys y como mejorar el flujo de trabajo solo con dos cosas básicas. Lo bueno de tmux, como todo linux, es que es hackeable y totalmente adaptable a tu manera de trabajar.