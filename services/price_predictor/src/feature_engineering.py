from typing import Optional

import pandas as pd
import talib

def add_features(
    X: pd.DataFrame,

    # hyper-parameters you can optimize through cross-validation
    # using a libray like Optuna
    rsi_timeperiod: Optional[int] = 14,
    momentum_timeperiod: Optional[int] = 14,
    volatility_timeperiod: Optional[int] = 5,    
) -> pd.DataFrame:
    """
    Adds the following features to the given DataFrame:
    - RSI indicator -> `rsi` column
    - Momentum indicator -> `momentum` column
    - Standard deviation -> `std` column

    Args:
        - X: pd.DataFrame: the input DataFrame
        - rsi_timeperiod: int: the time period for the RSI indicator
        - momentum_timeperiod: int: the time period for the momentum indicator
        - volatility_timeperiod: int: the time period for the standard deviation    

    Returns:
        - pd.DataFrame: the input DataFrame with the new columns
    """
    X_ = add_momentum_indicators(X, rsi_timeperiod, momentum_timeperiod)
    X_ = add_volatility_indicators(X_, timeperiod=volatility_timeperiod)

    return X_

def add_momentum_indicators(
    X: pd.DataFrame,
    rsi_timeperiod: Optional[int] = 14,
    momentum_timeperiod: Optional[int] = 14,
) -> pd.DataFrame:
    """
    Adds the
    - RSI indicator -> `rsi` column
    - Momentum indicator -> `momentum` column
    to the given DataFrame.

    Args:
        - X: pd.DataFrame: the input DataFrame
    
    Returns:
        - pd.DataFrame: the input DataFrame with the new columns
    """
    X_ = X.copy()
    X_['rsi'] = talib.RSI(X_['close'], timeperiod=rsi_timeperiod)
    X_['momentum'] = talib.MOM(X_['close'], timeperiod=momentum_timeperiod)

    return X_


def add_volatility_indicators(
    X: pd.DataFrame,
    timeperiod: Optional[int] = 5,
    nbdev: Optional[int] = 1,
) -> pd.DataFrame:
    """
    Adds a new column with the standard deviation to capture volatility in
    the market
    """
    X_ = X.copy()

    X_['std'] = talib.STDDEV(X_['close'], timeperiod=timeperiod, nbdev=nbdev)

    return X_