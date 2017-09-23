"""
created: 9/22/2017
(c) copyright 2017 Synacor, Inc

Callbacks for reporting progress during training
"""
from neon.callbacks.callbacks import Callback
from neon.transforms.cost import MultiMetric, Misclassification, LogLoss


class TrainingProgress(Callback):
    """
    progress callback
    """
    def __init__(self, valid):
        super(TrainingProgress, self).__init__(epoch_freq=1)
        self.valid = valid
        self.exclusive_metric = MultiMetric(Misclassification(), 1)
        self.overlapping_metric = MultiMetric(LogLoss(), 0)

    def on_epoch_end(self, callback_data, model, epoch):
        """
        Called when an epoch is about to end. This is where we shuffle the training data.

        Arguments:
            callback_data (HDF5 dataset): shared data between callbacks
            model (Model): model object
            epoch (int): index of epoch that is ending
        """
        print('Exclusive class misclassification error = {}%'.format(
            model.eval(self.valid, metric=self.exclusive_metric).get()[0,0] * 100))
        print('Overlapping class log loss error = {}'.format(model.eval(self.valid, metric=self.overlapping_metric)))
