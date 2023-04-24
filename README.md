# Proyecto 1 - Parte Web

<p align="center">
<img width="460" height="400" src="maze logo.jpg">
</p>

<details open>
  <summary>Contenido:</summary>
  <ol>
    <li><a href="#descripción-y-características">
      Descripción y características 
      <ul>
        <li><a href="#descripción-del-proyecto">Descripción del proyecto</a></li>
        <li><a href="#características-principales">Características principales</a></li>
      </ul>
    </a></li>
    <li><a href="#requisitos-e-instalación">
      Requisitos e Instalación
      <ul>
        <li><a href="#requisitos">Requisitos</a></li>
        <li><a href="#guía-de-instalación">Guía de instalación</a></li>
      </ul>
    </a></li>
    <li><a href="#instrucciones-de-uso">
      Instrucciones de uso
    </a></li>
    <li><a href="#licencia-de-uso">
      Licencia de uso
    </a></li>
    <li><a href="#diagramas">
      Diagramas
      <ul>
        <li><a href="#diagrama-de-clases">Diagrama de clases</a></li>
        <li><a href="#diagrama-de-flujo">Diagrama de flujo</a></li>
      </ul>
    </a></li>
    <li><a href="#link-de-video-de-presentación">
      Link de video de presentación
    </a></li>
    <li><a href="#autores">
      Autores
    </a></li>
    <li><a href="#bibliografía">
      Bibliografía
    </a></li>
  </ol>
</details>

---

## Descripción y características 

### Descripción del proyecto:

El proyecto presentado a continuación se trata de la implementación de un juego sencillo basado en el ejemplo encontrado en (https://www.mysteinbach.ca/game-zone/1507/maze/).
La finalidad del mismo es servir de muestra del uso de POO , programación genérica y concurrente, además del uso de distintos patrones de diseño. A su vez cabe resaltar que el programa se hizo pensando en que pueda funcionar en la consola, aunque por su propia estructura , dicha salida y entrada (consola) puede cambiarse y con algunas modificaciones puede utilizarse otros entornos(algun entorno gráfico).
Por último , cabe resaltar que , aunque el juego en sí aparenta cierta simpleza , su implementacion intenta ser robusta y prima el enfoque en la arquitectura del mismo. Se prioriza por ello la extensibilidad y portabilidad de programa.

### Características principales:

El programa consta de 4 interfaces:
+ Menu: Con las flechas de arriba (W) y abajo (S) del jugador 1 ,se mueve el seleccionador del menu. Se presiona ENTER para seleccionar el tipo de juego que desea.
+ Pantalla p1 vs p2: El jugador 1 (caracter A) se mueve con W A S D y el jugador (caracter B) con I K J L. El jugador realiza su movimiento en su turno, el turno se verifica en la parte superior del mapa. Una vez el jugador presiona alguna tecla , su turno acaba y pasa a jugar el otro jugador. Gana quien llegue al objetivo primero, esto se verá reflejado en un mensaje que indica el ganador de la partida.
+ Pantalla p1 vs pc: Igual que el anterior, solo que la pc jugará automáticamente cuando sea su turno.
+ Pantalla p1 vs reloj: el jugador 1 juega contra el reloj. Tiene 20 segundos para ganar. Si el juego acaba sin completar el recorrido, declara al juego como partida perdida.

Se puede notar en los tres juegos que el jugador 1 está representado por el caracater A y el jugador 2 , por el B. El laberinto consta de las paredes simbolizadas con 'X' y el espacio ' ' , tambien cabe rasaltar que hay una caracter '#' que representa el objetivo.


## Requisitos e Instalación

### Requisitos:

+ Sistema operativos Linux o Windows
+ Computadora de gama baja
+ Compilador g++ v20 o posterior
+ Administrador de paquetes Cmake v3 o posterior

### Tecnología utilizada:
+ [C++](https://devdocs.io/cpp/) - Lenguaje de programacion utilizado
+ [VS Code](https://code.visualstudio.com/) - Editor de código Utilizado

### Guía de instalación:

Clonación de repositorio con:

```bash
git clone https://github.com/CS1103/proyecto-final-2023_0-proyecto-final-2023_0-grupo-2.git
```


## Instrucciones de uso:

Una vez iniciado el programa la forma de interactuar con el mismo se reduce a las teclas:
+ W A S D : Flechas del jugador 1 (p1)
+ I K J L : Flechas del jugador 2 (p2)
+ ENTER: Entrar (ambos jugadores)   

El juego consta de 2 mapas:
+ mapa1 = un tablero de 21x15
+ mapa2 = un tablero de 42x30

Abrir la consola y ejecutar el comando: ./main 

Se mostrará el siguiente mensaje: INGRESE EL MAPA que desea jugar:  (deberá escribir mapa1 o mapa2)

Finalmente se verá el menu y podrá elegir el modo de juego.


## Licencia de uso:

Distribuido bajo la licencia MIT. Ver [`LICENSE`](LICENSE) para más información.

## Diagramas:

### Diagrama de clases: 

![Diagrama de clases](Dclases.jpeg)

### Diagrama de flujo:

Presentamos el bucle principal en el que se basa toda la interacción de cada interfaz.
![Diagrama de flujo](Dflujo.jpeg)

## Link de video de presentación:

https://youtu.be/nkVhM3Y2_gY

## Autores:
+ Bladimir Alferez Vicente
+ Autor 2 
+ Autor 3
+ Autor 4
+ Autor 5

## Bibliografía

+ Freeman, E., Robson, E., Bates, B., & Sierra, K. (2004). Head first design patterns. O'Reilly Media, Inc.
+ Dusseault, L. (2006). Practical C++ programming. O'Reilly Media, Inc.
+ Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1995). Design patterns: Elements of reusable object-oriented software. Addison-Wesley Professional.
+ Meyer, B. (1997). Object-oriented software construction (2nd ed.). Prentice Hall.
