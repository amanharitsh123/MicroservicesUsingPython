# MicroservicesUsingPython

A simple microservice application using python that I coded over a weekend. There are 4 microservices here in this project admin, main, rabbitmq and frontend.

This project is a simple implementation of a E-store where we have "admin" service which provides CRUD options for the products and "main" provides api's
which are to view all products and provide the "like" capabilities for a product. 

"frontend" microservice provides a very simple html page which allows CRUD over the products and like option as well.

Databases of "admin" and "main" are kept in sync using a producer consumer model with RabbitMQ.

"admin" is implemented using Django whereas "main" is implemented using Flask.

Note: I have referred many online resources for "main" and "admin" microservices in this project specifically freecodecamp video. 
