import re

import customLogger

class Parser:

    def parse_arg(args):
        '''
        Parse system arguments.
        '''
        logger = customLogger.gen_logging('', 'info')

        if type(args) != list:
            args = args.split()[1:]
        else:
            args = args[1:]
        cmd = {}

        try:
            int(args[0])
        finally:
            cmd['N'] = args[0]
            cmd['T'] = args[1]
            cmd['alpha'] = args[2]
            cmd['beta'] = args[3]
            cmd['gamma'] = args[4]
            cmd['phi'] = args[5]
            cmd['delta'] = args[6]


        def subls_modes(ls):
            for arg in ls:
                if not re.match(r'--\d', arg) and '=' not in arg:
                    return
                yield arg

        def sub_ls_mode(ls):
            if re.match(r'--\d', ls[0]):
                ls = ls[1:]
            for arg in ls:
                if re.match(r'--\d', arg):
                    return
                yield arg

        for i in range(len(args)):
            if args[i] == '-import' or args[i] == '--i':
                if args[+ 1][0] == '-' or args[i + 1][0:2] == '--':
                    logger.info("Invalid setting file name specified. ")
                else:
                    # print(os.getcwd())  # To debug when file cannot be fetched.
                    cmd['import setting'] = args[i + 1]
            if args[i] == '-test_rate':
                cmd['test rate'] = args[i + 1]
            if args[i] == '-immune_time':
                cmd['immune time'] = args[i + 1]
            if args[i] == '-m':
                cmd['modes'] = {}
                modes_tmp = list(subls_modes(args[i + 1:]))
                # print(modes_tmp)
                for i in range(len(modes_tmp)):
                    if re.match(r'--\d', modes_tmp[i]):
                        cmd['modes'][int(modes_tmp[i][2:])] = list(sub_ls_mode(modes_tmp[i:]))
            if args[i] == '-verbose' or args[i] == '--v':
                if args[i + 1] in ['debug', 'info', 'error']:
                    cmd['logger_level'] = args[i + 1]
                else:
                    cmd['logger_level'] = 'info'
            if args[i] == '-f':
                if args[i + 1] == 'run':
                    raise ValueError('Invalid file name: "run". ')
                if not(args[i + 1][0] == '-' or args[i + 1][0:2] == '--'):
                    cmd['filename'] = args[i + 1]
            if args[i] == 'run':
                cmd['express'] = True

        return cmd