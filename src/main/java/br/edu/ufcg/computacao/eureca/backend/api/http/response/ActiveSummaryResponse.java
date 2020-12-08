package br.edu.ufcg.computacao.eureca.backend.api.http.response;

import br.edu.ufcg.computacao.eureca.backend.constants.ApiDocumentation;
import io.swagger.annotations.ApiModelProperty;

public class ActiveSummaryResponse {
    @ApiModelProperty(position = 0, example = ApiDocumentation.Model.REGISTRATION)
    String registration;
    @ApiModelProperty(position = 1, example = ApiDocumentation.Model.PERIOD)
    String admissionTerm;
    @ApiModelProperty(position = 2, example = ApiDocumentation.Model.NUMBER)
    int termsCompleted;
    @ApiModelProperty(position = 3, example = ApiDocumentation.Model.PERCENTAGE)
    double progress;

    public ActiveSummaryResponse(String registration, String admissionTerm, int termsCompleted, double progress) {
        this.registration = registration;
        this.admissionTerm = admissionTerm;
        this.termsCompleted = termsCompleted;
        this.progress = progress;
    }

    public String getRegistration() {
        return registration;
    }

    public void setRegistration(String registration) {
        this.registration = registration;
    }

    public String getAdmissionTerm() {
        return admissionTerm;
    }

    public void setAdmissionTerm(String admissionTerm) {
        this.admissionTerm = admissionTerm;
    }

    public int getTermsCompleted() {
        return termsCompleted;
    }

    public void setTermsCompleted(int termsCompleted) {
        this.termsCompleted = termsCompleted;
    }

    public double getProgress() {
        return progress;
    }

    public void setProgress(double progress) {
        this.progress = progress;
    }
}