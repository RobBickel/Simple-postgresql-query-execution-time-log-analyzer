#!/usr/bin/env python
import sys
import re
import collections

STATEMENT_STRING = "STATEMENT:"
DURATION_BEGINNING_STRING = "CEST LOG:  duration: "
DURATION_BEGINNING_STRING_LENGTH = len(DURATION_BEGINNING_STRING)
REGEX_MATCH_FLOAT = "([0-9]*[.])[0-9]+"

query_to_time_executions_dictionary = dict()
line_counter = 0
last_command = ""


def readline_and_count():
    global line_counter
    line_counter += 1
    return f.readline()


class QueryDetails(object):
    durations = []
    line_numbers = []

    def __init__(self, durations, line_numbers):
        self.durations = durations
        self.line_numbers = line_numbers


if len(sys.argv) != 2:
    print "You need to pass filename as argument"
    sys.exit(0)


f = open(str(sys.argv[1]))
line = f.readline()

while line:
    line = readline_and_count()

    if line.find(STATEMENT_STRING) != -1:
        command = line[line.find(STATEMENT_STRING):]
        if query_to_time_executions_dictionary.has_key(command):
            query_to_time_executions_dictionary[command].line_numbers.append(line_counter)
        else:
            query_to_time_executions_dictionary[command] = QueryDetails([], [line_counter])
        last_command = command

    elif line.find(DURATION_BEGINNING_STRING) != -1:
        duration_string_with_unit = line[line.find(DURATION_BEGINNING_STRING) + DURATION_BEGINNING_STRING_LENGTH:]
        duration_number = float(re.search(REGEX_MATCH_FLOAT, duration_string_with_unit).group(0))
        durations = query_to_time_executions_dictionary[last_command].durations
        durations.append(duration_number)
        query_to_time_executions_dictionary[last_command].durations = durations

f.close()

number_of_occurances_to_query = dict()
time_of_execution_to_query = dict()

for query, details in query_to_time_executions_dictionary.iteritems():
    number_of_occurances_to_query[len(details.line_numbers)] = query

for query, details in query_to_time_executions_dictionary.iteritems():
    for time_execution in details.durations:
        time_of_execution_to_query[time_execution] = query

# print time of execution -> query
time_of_execution_to_query = collections.OrderedDict(sorted(time_of_execution_to_query.items()))
for time_of_execution, query in time_of_execution_to_query.iteritems():
    print str(time_of_execution) + "  " + query
    print "\n\n\n"

# print number of executions -> query
# number_of_occurances_to_query = collections.OrderedDict(sorted(number_of_occurances_to_query.items()))
# for number_of_occurances, query in number_of_occurances_to_query.iteritems():
#     print str(number_of_occurances) + "  " + query
#     print "\n\n\n"
