import sys
import matplotlib.pyplot as plt
import numpy as np

# np.random.seed(1)

def simulate_regime_change(stdev, output_filename, plot=False):
    '''Simulate two adjacent regimes.

    XY data, collected every minute of the day, where Y in linearly
    dependent on X with some noise, and

    Presuming a regime shift at minute of the day change_minute, the regimes may be characterized by
    where `e` is a normal distribution of errors characterized by a standard deviation `s` that is
    constant throughout the day:

        Y1 = a1 * X1 + b1 + e(s) for minute of day < change_minute
        Y2 = a2 * X2 + b2 + e(s) for minute of day >= change_minute

    The regime change happens between 06:00 and 18:00 i.e. `360 <= changeMinute <= 1080`.

    The X data is produced uniformly on the half-open interval [0.0, 1.0). The gradients and
    intercepts are chosen uniformly from the half-open intervals [0.0, gradient_upper_bound) and
    [0.0, intercept_upper_bound) respectively.

    Arguments:
        stdev [float]:
            the standard deviation of the normal distribution of errors (NB: must be greater than 0)
        output_filename [string]:
            the filename you want to write to
        plot [boolean]:
            if passed, plot the two regimes.

    Returns:
        change_minute, X, Y
    '''
    series_length = 1440
    gradient_upper_bound = 1.0
    intercept_upper_bound = 0.1

    # Parameterize regimes
    a1, a2 = gradient_upper_bound * np.random.random(2)
    b1, b2 = intercept_upper_bound * np.random.random(2)
    change_minute = np.random.randint(
            np.around(series_length / 4.0), np.around(3 * series_length / 4.0))

    # Populate regimes
    regime1_x = np.random.random(change_minute)
    regime2_x = np.random.random(series_length - change_minute)
    regime1_y = a1 * regime1_x + b1 + np.random.normal(loc=0, scale=stdev, size=len(regime1_x))
    regime2_y = a2 * regime2_x + b2 + np.random.normal(loc=0, scale=stdev, size=len(regime2_x))

    # Output
    if plot:
        plt.plot(regime1_x, regime1_y, 'r.', label='regime1')
        plt.plot(regime2_x, regime2_y, 'b.', label='regime2')
        plt.legend()
        plt.savefig('{}.png'.format(output_filename))

    x = np.hstack([regime1_x, regime2_x])
    y = np.hstack([regime1_y, regime2_y])

    header = '# series_length={:d}, stdev={:.2e}\n'.format(series_length, stdev)
    header += '# a1={:.2e}, b1={:.2e}, a2={:.2e}, b2={:.2e}\n'.format(a1, b1, a2, b2)
    header += '# Regime shift at minute {:d}\n'.format(change_minute)
    output_file = open(output_filename, 'w')
    output_file.write(header)
    output_file.writelines(['{:.3e} {:.3e}\n'.format(_x, _y) for _x, _y in zip(x, y)])
    output_file.close()

    return change_minute, x, y


from sklearn.linear_model import LinearRegression


actual_change_minute , x, y = simulate_regime_change(0.01, 'S_0.01', plot=True)

plt.figure()
plt.scatter(x, y)
plt.show()
initial_window_size = 360
step = 10

x0 = x[:initial_window_size]
x0 = np.reshape(x0, (x0.shape[0],1))
y0 = y[:initial_window_size]
y0 = np.reshape(y0, (y0.shape[0],1))


model = LinearRegression()

regime0 = model.fit(x0,y0)

params = np.append(regime0.intercept_,regime0.coef_)
prediction = regime0.predict(x0)

new_X = np.append(np.ones((len(x0),1)),x0,axis = 1)

from scipy import stats
MSE = (sum((y0-prediction)**2))/(len(new_X)-len(new_X[0]))

# Note if you don't want to use a DataFrame replace the two lines above with
# newX = np.append(np.ones((len(X),1)), X, axis=1)
# MSE = (sum((y-predictions)**2))/(len(newX)-len(newX[0]))

var_b = MSE*(np.linalg.inv(np.dot(new_X.T,new_X)).diagonal())
sd_b = np.sqrt(var_b)
ts_b = params/ sd_b

p_values =[2*(1-stats.t.cdf(np.abs(i),(len(new_X)-len(new_X[0])))) for i in ts_b]

p_values = np.round(p_values,3)
p_values

# while initial_window_size < len :
    


# if __name__ == '__main__':
#     ''' Simulate a regime change.

#     Usage:
#         python simulate-regime-change.py 0.01 xy.dat, or
#         python simulate-regime-change.py 0.01 xy.dat plot
#     '''
#     if len(sys.argv) <= 2:
#         raise ValueError('Invalid arguments: please see inline documentation')
#     simulate_regime_change(float(sys.argv[1]), *sys.argv[2:])
