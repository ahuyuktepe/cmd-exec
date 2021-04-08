## 1 Introduction
### 1.1 Installation
Add content here

### 1.2 Directory Structure
This python module expects following directories in the root directory of the project.
```
- logs
- modules
- resources
    - arguments
    - commands
    - configs
```
| Directory Name   | Description                         |
|------------------|-------------------------------------|
| logs             | This directory contains log files.  |
| modules          | This directory contains custom modules to be used.  |
| resources        | This directory contains all files which are used as input while executing command.  |
| arguments        | This directory contains yaml files which provides arguments to the command to be executed. |
| commands         | This directory contains yaml files which provides command information to be executed. |
| configs          | This directory contains yaml files which provides generic configurations to be imported. |

### 1.3 Main Configuration
Main configuration is a yaml file which contains required configurations for command executor to run. 

### 1.3.1 Log Settings
This property provides information about logging feature.

#### level
Default level of log which will decide whether to write the given message in log file.
Available Values 
- info
- warn
- error
Default: info
  
#### dir_path
Path of the log file.
Default: logs

#### file_name	
Log file name.
Default: main

#### max_size
Maximum size of log file.
Default: 1 MB

#### msg_format	
Format of log message.
Default: {level} : {msg}

#### date_format
Format of date to be displayed in log message.
Default: %Y-%m-%d %H:%M:%S

### 1.3.2 Log Settings
This property provides mapping from field type to associated class.

Following are the default field types.

| Type        | Class                               |
|-------------|-------------------------------------|
| date        | DateField                           |
| text        | TextField                           |
| selection   | SelectionField                      |

#### DateField

| Property    | Description                                      |
|-------------|--------------------------------------------------|
| required    | If true, value should be provided.Default: False |
| format      | Date format. Default: %m-%d-%Y                   |
| min         | Minimum date can be allowed.                     |
| max         | Maximum date can be allowed.                     |
| default     | Default value.                                   |

#### TextField

| Property    | Description                                      |
|-------------|--------------------------------------------------|
| required    | If true, value should be provided.Default: False |
| min         | Minimum date can be allowed.                     |
| max         | Maximum date can be allowed.                     |
| default     | Default value.                                   |

#### SelectionField

| Property    | Description                                      |
|-------------|--------------------------------------------------|
| required    | If true, value should be provided.Default: False |
| min         | Minimum number of selected option count.         |
| max         | Maximum number of selected option count.         |
| default     | Default value.                                   |

## 1.4 Modes
Add content here

