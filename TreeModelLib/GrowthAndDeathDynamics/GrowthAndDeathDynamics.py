#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class GrowthAndDeathDynamics:
    ## Concept for tree growth and death dynamics
    #  @VAR case: tree dynamic concept to be used for the model
    #  @date: 2019 - Today
    #  @author: jasper.bathmann@ufz.de

    def __init__(self, case):
        if case == "SimpleTest":
            return 0
        else:
            raise KeyError("Required competition not implemented.")
