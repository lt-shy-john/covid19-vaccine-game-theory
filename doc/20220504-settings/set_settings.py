for i in range(11):
    a1 = i * 10
    for j in range(11):
        a2 = j * 10
        filename = f'settings_a01-{str(a1).zfill(3)}_a02-{str(a2).zfill(3)}.txt'

        with open(filename, 'w') as f:
            f.write('# Vaccines\n')
            f.write('## Vaccine\n')
            f.write('Name: Sample-vaccine-1\n')
            f.write('dose: 1\n')
            f.write('days: 28\n')
            f.write('vaccine-type:\n')
            f.write('cost: 0\n')
            f.write('efficacy: 0.95\n')
            f.write(f'alpha: {a1/100}\n')
            f.write('beta: 0\n')
            f.write('gamma: 0\n')
            f.write('delta: 0\n')
            f.write('phi: 0.0055\n')
            f.write('## Vaccine\n')
            f.write('Name: Sample-vaccine-1\n')
            f.write('dose: 2\n')
            f.write('days: 28\n')
            f.write('vaccine-type:\n')
            f.write('cost: 0\n')
            f.write('efficacy: 0.83\n')
            f.write(f'alpha: {a2/100}\n')
            f.write('beta: \n')
            f.write('gamma:\n')
            f.write('delta:\n')
            f.write('phi: 0.0074\n')
            f.write('## Vaccine supply\n')
            f.write('file: vaccine_supply.csv')