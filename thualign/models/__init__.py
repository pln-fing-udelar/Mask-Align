# Copyright 2021-Present The THUAlign Authors
import thualign.models.agreement_wrapper
import thualign.models.mask_align
import thualign.models.transformer_align


def get_model(params):
    name = params.model.lower()

    if name == "transformer_align":
        model_cls = thualign.models.transformer_align.TransformerAlign
    elif name == 'mask_align':
        model_cls = thualign.models.mask_align.MaskAlign
    else:
        raise LookupError("Unknown model %s" % name)

    if getattr(params, "agree_training", False):
        return thualign.models.agreement_wrapper.AgreementWrapper.build_model(params, model_cls)
    else:
        return model_cls.build_model(params)
