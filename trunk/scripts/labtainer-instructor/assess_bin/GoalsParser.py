#!/usr/bin/env python3
'''
This software was created by United States Government employees at 
The Center for Cybersecurity and Cyber Operations (C3O) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
  1. Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
'''
'''
  GoalsParser.py
  Description: * Read goals.config and create the goals.json file
               * with values specific to this student (parameterized).
'''
import json
import glob
import os
import random
import sys
import MyUtil
import ParameterParser

MYHOME = ""
answer_tokens=['result', 'parameter', 'parameter_ascii']
logger = None

class MyGoal(object):
    """ Goal - goalid, goaltype, goaloperator, answertag, resulttag, boolean_string, goal1tag, goal2tag """
    goalid = ""
    goaltype = ""
    goaloperator = ""
    answertag = ""
    resulttag = ""
    boolean_string = ""
    goal1tag = ""
    goal2tag = ""

    def goal_dict(object):
        return object.__dict__

    def __init__(self, goalid, goaltype, goaloperator="", answertag="", 
                 resulttag="", boolean_string="", goal1tag="", goal2tag=""):
        self.goalid = goalid
        self.goaltype = goaltype
        self.goaloperator = goaloperator
        self.answertag = answertag
        self.resulttag = resulttag
        self.boolean_string = boolean_string
        self.goal1tag = goal1tag
        self.goal2tag = goal2tag

def getTagValue(parameter_list, target, finaltag, logger):
    if target == "answer":
        returnTagValue = 'answer=%s' % finaltag
    else:
        if target.startswith('parameter'):
            if finaltag not in parameter_list:
                logger.error('Could not find parameter %s' % finaltag)
                sys.exit(1)
            value = parameter_list[finaltag]
            if target.lower() == "parameter_ascii":
                if '0x' in value:
                    num = int(value, 16)
                else: 
                    num = int(value)
                if num not in range(41, 177):
                    logger.error('parameter_ascii value %s not in ascii range' % value)
                    sys.exit(1)
                value = chr(num)
            returnTagValue = 'answer=%s' % value
        else:
            returnTagValue = '%s.%s' % (target, finaltag)
    return returnTagValue


def ValidateTag(parameter_list, studentdir, goal_type, inputtag, allowed_special_answer, logger):
    # if allowed_special_answer is true, then allow 'answer=<string>'
    # UNLESS if the goal_type is matchacross
    returntag = ""
    if '=' in inputtag:
        if not allowed_special_answer:
            logger.error("goals.config only answertag is allowed answer=<string>, resulttag (%s) is not" % inputtag)
            sys.exit(1)
        if goal_type == "matchacross":
            logger.error("goals.config answer=<string> and goal_type==matchacross is not allowed")
            sys.exit(1)
        (target, finaltag) = inputtag.split('=')
        returntag = getTagValue(parameter_list, target, finaltag, logger)
 
    elif inputtag.startswith('(') and inputtag.endswith(')'):
        returntag = 'result.%s' % inputtag
    elif '.' in inputtag:
        #logger.debug("tag %s contains '.'" % inputtag)
        (target, finaltag) = inputtag.split('.')
        if not target in answer_tokens:
            logger.error("goals.config tag=<string> then tag must be:(%s), got %s" % (','.join(answer_tokens), inputtag))
            sys.exit(1)
        if not MyUtil.CheckAlphaDashUnder(finaltag):
            logger.error("Invalid characters in goals.config's tag (%s)" % inputtag)
            sys.exit(1)

        returntag = getTagValue(parameter_list, target, finaltag, logger)
    else:
        #logger.debug("tag is %s" % inputtag)
        if not MyUtil.CheckAlphaDashUnder(inputtag):
            logger.error("Invalid characters in goals.config's tag (%s)" % inputtag)
            sys.exit(1)
        returntag = 'result.%s' % inputtag

    return returntag

def GetLabInstanceSeed(studentdir, logger):
    seed_dir = os.path.join(studentdir, ".local",".seed")
    student_lab_instance_seed = None
    if os.path.isfile(seed_dir):
        with open(seed_dir) as fh:
            student_lab_instance_seed = fh.read().strip()
        if student_lab_instance_seed is None:
            logger.error('could not get lab instance seed from %s' % seed_dir)
            #sys.exit(1)
    return student_lab_instance_seed

def ParseGoals(homedir, studentdir, logger_in):
    MYHOME = homedir
    logger = logger_in
    nametags = []
    configfilename = os.path.join(MYHOME,'.local','instr_config', 'goals.config')
    configfile = open(configfilename)
    configfilelines = configfile.readlines()
    configfile.close()
    lab_instance_seed = GetLabInstanceSeed(studentdir, logger)
    if lab_instance_seed is None:
        logger.debug('No lab instance seed, not grading %s' % studentdir)
        print('No lab instance seed, not grading %s' % studentdir)
        return
    container_user = ""
    param_filename = os.path.join(MYHOME, '.local', 'config',
          'parameter.config')

    pp = ParameterParser.ParameterParser(None, container_user, lab_instance_seed, logger)

    parameter_list = pp.ParseParameterConfig(param_filename)

    for line in configfilelines:
        linestrip = line.rstrip()
        if linestrip:
            if not linestrip.startswith('#'):
                #logger.debug("Current linestrip is (%s)" % linestrip)
                try:
                    (each_key, each_value) = linestrip.split('=', 1)
                except:
                     logger.error('goal lacks "=" character, %s' % linestrip)
                     sys.exit(1)
                each_key = each_key.strip()
                if not MyUtil.CheckAlphaDashUnder(each_key):
                    logger.error("Invalid characters in goals.config's key (%s)" % each_key)
                    sys.exit(1)
                if len(each_key) > 15:
                    logger.debug("goal (%s) is more than 15 characters long\n" % each_key)

                values = []
                # expecting - either:
                # <type> : <operator> : <resulttag> : <answertag>
                # <type> : <goal1tag> : <goal2tag>
                # <type> : <string>
                values = each_value.split(" : ")
                numvalues = len(values)
                #logger.debug('numvalues is %d  values are: %s' % (numvalues, str(values)))
                if not (numvalues == 4 or numvalues == 3 or numvalues == 2):
                    logger.error("goals.config contains unexpected value (%s) format" % each_value)
                    sys.exit(1)
                if numvalues == 4:
                    ''' <type> : <operator> : <resulttag> : <answertag> '''
                    goal_type = values[0].strip()
                    goal_operator = values[1].strip()
                    resulttag = values[2].strip()
                    answertag = values[3].strip()
                    # Allowed 'answer=<string>' for answertag only
                    valid_answertag = ValidateTag(parameter_list, studentdir, goal_type, answertag, True, logger)
                    valid_resulttag = ValidateTag(parameter_list, studentdir, goal_type, resulttag, False, logger)
                    if not (goal_type == "matchany" or
                        goal_type == "matchlast" or
                        goal_type == "matchacross" or
                        goal_type == "count" or
                        goal_type == "value" or
                        goal_type == "valueSum" or
                        goal_type == "valueMax" or
                        goal_type == "execute"):
                        logger.error("Error found in line (%s)" % linestrip)
                        logger.error("goals.config contains unrecognized type (1) (%s)" % goal_type)
                        sys.exit(1)
                    if not (goal_type == "execute"):
                        # If goal_type is not 'execute' then check the goal_operator
                        if not (goal_operator == "string_equal" or
                            goal_operator == "hash_equal" or
                            goal_operator == "string_diff" or
                            goal_operator == "string_start" or
                            goal_operator == "string_end" or
                            goal_operator == "string_contains" or
                            goal_operator == "integer_equal" or
                            goal_operator == "integer_greater" or
                            goal_operator == "integer_lessthan"):
                            logger.error("Error found in line (%s)" % linestrip)
                            logger.error("goals.config contains unrecognized operator (%s)" % (goal_operator))
                            sys.exit(1)
                    else:
                        # Make sure the file to be executed exist
                        execfile = os.path.join(MYHOME, '.local', 'bin', goal_operator)
                        if not (os.path.exists(execfile) and os.path.isfile(execfile)):
                            logger.error("Error found in line (%s)" % linestrip)
                            logger.error("goals.config contains execute goals with missing exec file (%s)" % (goal_operator))
                            sys.exit(1)
                    nametags.append(MyGoal(each_key, goal_type, goaloperator=goal_operator, answertag=valid_answertag, resulttag=valid_resulttag))
                    #print "goal_type non-boolean"
                    #print nametags[each_key].goal_dict()
                elif numvalues == 3:
                    ''' <type> : <goal1tag> : <goal2tag> '''
                    goal_type = values[0].strip()
                    if goal_type == 'time_before' or goal_type == 'time_during' or goal_type == 'time_not_during':
                        goal1tag = values[1].strip()
                        goal2tag = values[2].strip()
                        nametags.append(MyGoal(each_key, goal_type, goal1tag=goal1tag, goal2tag=goal2tag))
                    elif goal_type == 'count_greater':
                        answertag = values[1].strip()
                        subgoal_list = values[2].strip()
                        nametags.append(MyGoal(each_key, goal_type, answertag=answertag, boolean_string=subgoal_list))
                    else:
                        logger.error('Could not parse goals.config line %s' % each_value)
                        sys.exit(1)
                    #print "goal_type non-boolean"
                    #print nametags[each_key].goal_dict()
                else:
                    ''' <type> : <string> '''
                    goal_type = values[0].strip()
                    if goal_type == 'boolean':
                        boolean_string = values[1].strip()
                        nametags.append(MyGoal(each_key, goal_type, boolean_string=boolean_string))
                    elif goal_type == 'is_true' or goal_type == 'is_false':
                        resulttag = values[1].strip()
                        #print('parsegoals type is %s result %s' % (goal_type, resulttag))
                        nametags.append(MyGoal(each_key, goal_type, resulttag=resulttag))
                    elif goal_type == 'count' or goal_type.startswith('value'):
                        resulttag = values[1].strip()
                        nametags.append(MyGoal(each_key, goal_type, resulttag=resulttag))
                    elif goal_type == 'count_greater':
                        logger.error('missing count_greater value in %s ?' % linestrip)
                        sys.exit(1)
                    else:
                        logger.error('Could not parse goals.config line %s' % linestrip)
                        sys.exit(1)
       
                    #print "goal_type boolean"
                    #print nametags[each_key].goal_dict()

                #nametags[each_key].toJSON()
                #nametags[each_key].goal_type = goal_type
                #nametags[each_key].goal_operator = goal_operator
                #nametags[each_key].answertag = valid_answertag
                #nametags[each_key].resulttag = valid_resulttag
                #nametags[each_key].boolean_string = boolean_string

        #else:
        #    print "Skipping empty linestrip is (%s)" % linestrip


    #print nametags["crash"].toJSON()
    #for (each_key, each_goal) in nametags.items():
    #    print nametags[each_key].toJSON()
    student_parent_dir = os.path.dirname(studentdir)
    resultsdir = os.path.join(student_parent_dir, '.local','result')
    try:
        os.makedirs(resultsdir)
    except:
        pass
    outputjsonfname = os.path.join(resultsdir,'goals.json')
    #print "GoalsParser: Outputjsonfname is (%s)" % outputjsonfname
        
    #print nametags
    jsonoutput = open(outputjsonfname, "w")
    jsondumpsoutput = json.dumps([x.goal_dict() for x in nametags], indent=4)
    jsonoutput.write(jsondumpsoutput)
    jsonoutput.write('\n')
    jsonoutput.close()

    return parameter_list

