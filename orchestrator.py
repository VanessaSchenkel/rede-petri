#!/usr/bin/env python
from Scheduler import Scheduler
from Event import Event
from Entity import Entity
from Resource import Resource
from random import randrange
import numpy as np 
from EntitySet import EntitySet
    
sch = Scheduler()
    
class CustomerGroup(Entity):
      def __init__(self, name, groupSize):
        super().__init__(name)
        self.groupSize = groupSize
        if groupSize == 1:
          self.tableType = 'Balcao'
        if groupSize == 2:
          self.tableType = 'Mesa para dois'
        if groupSize > 2:
          self.tableType = 'Mesa para quatro'
    
      def setTableType(self, tableType):
        self.tableType = tableType
    
      def getTableType(self):
        return self.tableType
    
class CustomerArrival(Event):
      def executeEvent(self, descriptors, model, groupSize):
        ### chose one of the queues, pay and order
        self.recordAmountOfClientsInTotal(model,   groupSize)
    
        customerGroup = model.createEntity("CustomerGroup", descriptors.entities, {'groupSize': groupSize})
        
        if model.getQueueSize("cashRegister1") > model.getQueueSize("cashRegister2"):
          model.insertInQueue("cashRegister2", customerGroup)
          if model.resources["Caixa2"].isAvailable():
            model.scheduleNow("CaixaServiceStart", descriptors.events, {'CaixaName': "Caixa2"})
        else:
          model.insertInQueue("cashRegister1", customerGroup)
          if model.resources["Caixa1"].isAvailable():
            model.scheduleNow("CaixaServiceStart", descriptors.events, {'CaixaName': "Caixa1"})
    
        if model.getTime() < 180.0:
          #generate new customers
          nextCustomerGroupSize = randrange(4)+1
          timeToNextArrival = np.random.exponential(3)
          model.scheduleIn("CustomerArrival", timeToNextArrival, descriptors.events, {'groupSize': nextCustomerGroupSize})
      
      def recordAmountOfClientsInTotal(self, model, groupSize):
        model.statistical.increaseDictLikeStatistic("Total de pessoas que comeram no restaurante: ", groupSize)
      def recordStatistics(self, model):
        model.statistical.increaseDictLikeStatistic("Número de grupos de clientes que chegaram: ", 1)
    
    
class CaixaServiceStart(Event):
      def executeEvent(self, descriptors, model, CaixaName):
        if model.resources[CaixaName].allocate(1):
          group = ""
          if CaixaName == "Caixa1":
            group = model.popFromQueue("cashRegister1")
          else:
            group = model.popFromQueue("cashRegister2")
    
          timeToNextEvent = np.random.normal(8,2)
          model.scheduleIn("CaixaServiceEnd", timeToNextEvent, descriptors.events, {'CaixaName': CaixaName, 'group': group})
      
      def recordStatistics(self, model):
        model.statistical.increaseDictLikeStatistic("Total de clientes que passaram pelos caixas: ", 1)
    
class CaixaServiceEnd(Event):
      def executeEvent(self, descriptors, model, CaixaName, group):
        model.resources[CaixaName].release(1)
        if CaixaName == 'Caixa1':
          if model.isQueueEmpty("cashRegister1") == False:
            model.scheduleNow("CaixaServiceStart", descriptors.events, {'CaixaName': "Caixa1"})
        else:
          if model.isQueueEmpty("cashRegister2") == False:
            model.scheduleNow("CaixaServiceStart", descriptors.events, {'CaixaName': "Caixa2"})
    
        print("Grupo na fila, " + group.getTableType() + ': ' + str(group.getId()))
        model.insertInQueue(group.getTableType(), group)
        if model.resources[group.getTableType()].isAvailable():
          model.scheduleNow("SitCustomerWaiting", descriptors.events, {'group': model.popFromQueue(group.getTableType())})
    
        model.insertInQueue("Kitchen", group)
    
        if model.resources['Cozinheiro'].isAvailable():
          model.scheduleNow("NewOrderStart", descriptors.events, {})
      
    
      def recordStatistics(self, model):
        model.statistical.increaseDictLikeStatistic("Amount of clients ended the Caixa service", 1)
    
class NewOrderStart(Event):
      def executeEvent(self, descriptors, model):
        if model.resources['Cozinheiro'].allocate(1):
          group = model.popFromQueue('Kitchen')
          timeToNextEvent = np.random.normal(14,5)
          model.scheduleIn("NewOrderEnd", timeToNextEvent,  descriptors.events, {'group':group})
    
      def recordStatistics(self, model):
        model.statistical.increaseDictLikeStatistic("Total de pedidos registrados: ", 1)
    
class NewOrderEnd(Event):
      def executeEvent(self, descriptors, model, group):
        #customer has to be seated to start eating right away, otherwise it needs to wait for the delivery
        model.resources['Cozinheiro'].release(1)
        if model.isEntityInQueueById('SeatedWaiting', group.getId()):
          model.scheduleNow("CustomerEats", descriptors.events, {'group': group})
        else:
          model.insertInQueue('OrderWaitingForDelivery', group)
          print('Terminou o pedido -> ' +  str(group.getId()))
    
        if model.isQueueEmpty('Kitchen') == False:
          model.scheduleNow("NewOrderStart", descriptors.events, {})
    
      def recordStatistics(self, model):
        model.statistical.increaseDictLikeStatistic("Total de pedidos finalizados: ", 1)
    
    
class CustomerEats(Event):
      def executeEvent(self, descriptors, model, group):
        print("Cliente " + str(group.getId()) + " comendo.")
        model.removeFromQueueById('SeatedWaiting', group.getId())
        model.insertInQueue('SeatedEating', group)
        timeToNextEvent = np.random.normal(20,8)
        model.scheduleIn("CustomerLeaving", timeToNextEvent,  descriptors.events, {'group':group})
    
      def recordStatistics(self, model):
        model.statistical.increaseDictLikeStatistic("Total de clientes que comeram: ", 1)
    
class CustomerLeaving(Event):
      def executeEvent(self, descriptors, model, group):
        print("Cliente " + str(group.getId()) + " indo embora")
        model.removeFromQueueById('SeatedEating', group.getId())
        model.resources[group.getTableType()].release(1)
        if model.isQueueEmpty(group.getTableType()) == False:
          print(" -> sentando cliente após outro cliente ir embora")
          model.scheduleNow("SitCustomerWaiting", descriptors.events, {'group': model.popFromQueue(group.getTableType())})
    
      def recordStatistics(self, model):
        model.statistical.increaseDictLikeStatistic("Grupo de clientes que sairam do restaurante: ", 1)
    
    
class SitCustomerWaiting(Event):
      def executeEvent(self, descriptors, model, group):
        if model.resources[group.getTableType()].isAvailable():
          model.resources[group.getTableType()].allocate(1)
          model.insertInQueue('SeatedWaiting', group)
          if model.isEntityInQueueById('OrderWaitingForDelivery', group.getId()):
            print("pedido pronto -> pode comer")
            model.scheduleNow("CustomerEats", descriptors.events, {'group': group})
        else:
          model.insertInQueue(group.getTableType(), group)
    
      def recordStatistics(self, model):
        model.statistical.increaseDictLikeStatistic("Grupos de clientes que sentaram na mesa: ", 1)
    
            
    
    
    
sch.defineResourceSpecialization('Caixa', Resource)
sch.defineResourceSpecialization('Mesa', Resource)
sch.defineResourceSpecialization('Cozinheiro', Resource)

sch.defineEntitySetSpecialization("cashRegister1", EntitySet)
sch.defineEntitySetSpecialization("cashRegister2", EntitySet)
sch.defineEntitySetSpecialization("Balcao", EntitySet)
sch.defineEntitySetSpecialization("Mesa para dois", EntitySet)
sch.defineEntitySetSpecialization("Mesa para quatro", EntitySet)
sch.defineEntitySetSpecialization("Kitchen", EntitySet)
sch.defineEntitySetSpecialization("SeatedWaiting", EntitySet)
sch.defineEntitySetSpecialization("SeatedEating", EntitySet)
sch.defineEntitySetSpecialization("UnseatedWaiting", EntitySet)

sch.initializeQueue("cashRegister1")
sch.initializeQueue("cashRegister2")
sch.initializeQueue("Balcao")
sch.initializeQueue("Mesa para dois")
sch.initializeQueue("Mesa para quatro")
sch.initializeQueue("Kitchen")
sch.initializeQueue("SeatedWaiting")
sch.initializeQueue("SeatedEating")
sch.initializeQueue("OrderWaitingForDelivery")

sch.createResource("Caixa", "Caixa1", 1)
sch.createResource("Caixa", "Caixa2", 1)
sch.createResource("Cozinheiro", "Cozinheiro", 3)
sch.createResource("Mesa", "Balcao", 6)
sch.createResource("Mesa", "Mesa para dois", 4)
sch.createResource("Mesa", "Mesa para quatro", 4)

sch.defineEventSpecialization('CustomerArrival', CustomerArrival)
sch.defineEventSpecialization('CaixaServiceStart', CaixaServiceStart)
sch.defineEventSpecialization('CaixaServiceEnd', CaixaServiceEnd)
sch.defineEventSpecialization('NewOrderStart', NewOrderStart)
sch.defineEventSpecialization('NewOrderEnd', NewOrderEnd)
sch.defineEventSpecialization('CustomerEats', CustomerEats)
sch.defineEventSpecialization('CustomerLeaving', CustomerLeaving)
sch.defineEventSpecialization('SitCustomerWaiting', SitCustomerWaiting)

sch.defineEntitySpecialization('CustomerGroup', CustomerGroup)

sch.scheduleNow('CustomerArrival', {'groupSize': 1})

sch.simulate()
