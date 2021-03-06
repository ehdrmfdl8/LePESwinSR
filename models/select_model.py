
"""
# --------------------------------------------
# define training model
# --------------------------------------------
"""


def define_Model(opt, scaler):
    model = opt['model']      # one input: L

    if model == 'plain':
        from models.model_plain import ModelPlain as M

    elif model == 'gan':     # one input: L
        from models.model_gan import ModelGAN as M

    elif model == 'degradation': # one input: H
        from models.model_degradation import ModelDegradation as M

    elif model == 'degradation_gan': # one input: H
        from models.model_degradation_gan import ModelDegradationGAN as M
    else:
        raise NotImplementedError('Model [{:s}] is not defined.'.format(model))

    m = M(opt, scaler)

    print('Training model [{:s}] is created.'.format(m.__class__.__name__))
    return m
