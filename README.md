# self-driving-car-jf-2020
> "Jugend forscht" is a German competition where young students are able to compete against each other with scientific projects.  
> This project was part of the 2020 competition in the Südwürttemberg region in January.  
> My first DHBW semester started right after I finished developing the car in winter 2019.

The "Self Driving Car" project describes the attempt to implant artificial intelligence into a toy car. The self-built RC car is equipped with an on-board computer, more precisely a Raspberry PI 3B, and three ultrasonic sensors.  

![Image](https://i.imgur.com/HFbsTnD.png "Toy car")
  
In order for the car to drive on its own, the Raspberry PI must run a special algorithm. But this is not just a simple algorithm, it is a pre-trained artificial intelligence. The "brain" of this AI consists of many different components. Important for this example, however, are the "weights", which are nothing more than a bunch of static numbers. Weights use mathematical operations to manage the brain's connections.

![Image](https://i.imgur.com/mpqsJYs.png "Toy car")
  
The distance values of the ultrasonic sensors are now transferred to this brain, whereupon the Raspberry PI can calculate the motor speed and the rotation value. This all happens several times per second.  
  
In previously executed simulations, the toy car is replicated and equipped with the same neural network. Here, too, the car is supposed to cover as long a distance as possible without errors. The only difference is that the weights were randomly generated at the beginning. After each generation of a simulated car, the weights are adjusted. Only the weights of the best two cars are mixed together.  

![Image](https://i.imgur.com/V6I849D.png "Toy car")
  
If you now let this computer simulation work for several hours, sooner or later you will get an optimal version of the car. To apply the trained neural network in reality, the weights of the best car must be adopted. To do this, the brain is replicated on the Raspberry PI and filled with the optimized weights. 
  
[Voila - a self-driving car.](https://www.ravensburg.dhbw.de/dhbw-ravensburg/aktuelles/detail/2020/2/voila-ein-selbstfahrendes-auto-platz-2-fuer-tim-bader-bei-jugend-forscht)

