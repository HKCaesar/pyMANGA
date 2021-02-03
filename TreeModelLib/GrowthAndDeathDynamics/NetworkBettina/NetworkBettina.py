#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""
from TreeModelLib.GrowthAndDeathDynamics import GrowthAndDeathDynamics
from TreeModelLib.GrowthAndDeathDynamics.SimpleBettina import SimpleBettina
import numpy as np


class NetworkBettina(SimpleBettina):
    ## NetworkBettina for death and growth dynamics. This module is implements ...
    #  @param Tags to define SimpleBettina: type
    #  @date 2019 - Today
    def __init__(self, args):
        case = args.find("type").text
        print("Growth and death dynamics of type " + case + ".")
        # self.rgf = tree.getRGF()
        # self.potential_partner = []
        # self.partner = []

    def progressTree(self, tree, aboveground_resources, belowground_resources):
        # network
        self.rgf  = tree.getRGF()
        self.partner = tree.getPartner()
        self.potential_partner = tree.getPotentialPartner()
        # network end
        geometry = tree.getGeometry()
        growth_concept_information = tree.getGrowthConceptInformation()
        self.parameter = tree.getParameter()
        self.r_crown = geometry["r_crown"]
        self.h_crown = geometry["h_crown"]
        self.r_root = geometry["r_root"]
        self.h_root = geometry["h_root"]
        self.r_stem = geometry["r_stem"]
        self.h_stem = geometry["h_stem"]
        self.survive = 1
        self.flowLength()
        self.treeVolume()
        self.treeMaintenance()
        self.bgResources(belowground_resources)
        self.agResources(aboveground_resources)
        self.growthResources()
        self.treeGrowthWeights()
        self.treeGrowth()
        geometry["r_crown"] = self.r_crown
        geometry["h_crown"] = self.h_crown
        geometry["r_root"] = self.r_root
        geometry["h_root"] = self.h_root
        geometry["r_stem"] = self.r_stem
        geometry["h_stem"] = self.h_stem
        growth_concept_information[
            "root_surface_resistance"] = self.root_surface_resistance
        growth_concept_information["xylem_resistance"] = self.xylem_resistance
        growth_concept_information["ag_resources"] = self.ag_resources
        growth_concept_information["bg_resources"] = self.bg_resources
        growth_concept_information["growth"] = self.grow
        growth_concept_information["available_resources"] = (
            self.available_resources)
        psi_zero = self.deltaPsi()
        growth_concept_information["psi_zero"] = psi_zero
        growth_concept_information["salinity"] = (
            (belowground_resources * psi_zero - psi_zero) / 85000000.)
        # network
        tree.setRGF(self.rgf)
        tree.setPotentialPartner(self.potential_partner)
        tree.setPartner(self.partner)
        print(belowground_resources)
        # network end
        tree.setGeometry(geometry)
        tree.setGrowthConceptInformation(growth_concept_information)
        if (self.survive == 1):
            tree.setSurvival(1)
        else:
            tree.setSurvival(0)

## This function calculates the available resources and the biomass increment.
    # In addition, this function reduces the available resources if trees are in the grafting process
    # and calls the root graft formation manager
    def growthResources(self):
        self.available_resources = min(self.ag_resources, self.bg_resources)
        self.grow = (self.parameter["growth_factor"] *
                     (self.available_resources - self.maint))
        if self.rgf != -1:
            print("here self.rgf != -1, " + str(self.rgf))
            self.grow = self.grow / 2
            self.rootGraftFormation()

        if (self.grow < 0):
            self.grow = 0
            self.survive = 0

    def rootGraftFormation(self):
        self.rgf = self.rgf + 1
        if self.rgf == 2:      # todo: correct threshold
            self.rgf = -1
            self.partner.append(self.potential_partner)
            self.potential_partner = []