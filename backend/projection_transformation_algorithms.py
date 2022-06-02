# This script re-implements the projection and transformation algorithm based on the project https://github.com/WinterKaro/iscmining-edoc17
# The algorithm is presented in the Paper "Discovering Instance-Spanning Constraints from Process Execution Logs based on Classification Techniques" by Karolin Winter and Stefanie Rinderle-Ma (https://ieeexplore.ieee.org/document/8089866).
# It takes one *.xes file and an event attribute as input and produces one or several *.arff files.
# The event attribute is used for dimension reduction, e.g. if there is more than one organizational resource (org:resource) in the log file, then one *.arff file per resource is produced. Otherwise the whole log is transferred into one *.arff file.
