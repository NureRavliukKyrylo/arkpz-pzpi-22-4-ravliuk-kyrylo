#ifndef KALMAN_FILTER_H
#define KALMAN_FILTER_H

class KalmanFilter {
private:
    float processNoise = 0.022;            
    float measurementNoise = 0.617;        
    float stateEstimate = 0;               
    float errorCovariance = 1;            

public:
    KalmanFilter() {}

    float filter(float measurement) {
        float predictedState = stateEstimate; 
        float predictedErrorCovariance = errorCovariance + processNoise;

        float kalmanGain = predictedErrorCovariance / 
                           (predictedErrorCovariance + measurementNoise); 

        stateEstimate = predictedState + kalmanGain * (measurement - predictedState);
        errorCovariance = (1 - kalmanGain) * predictedErrorCovariance;

        return stateEstimate;
    }
};

#endif
