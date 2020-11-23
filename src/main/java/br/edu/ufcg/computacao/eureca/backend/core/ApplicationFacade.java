package br.edu.ufcg.computacao.eureca.backend.core;

import br.edu.ufcg.computacao.eureca.as.core.AuthenticationUtil;
import br.edu.ufcg.computacao.eureca.as.core.models.SystemUser;
import br.edu.ufcg.computacao.eureca.backend.api.http.response.*;
import br.edu.ufcg.computacao.eureca.backend.constants.*;
import br.edu.ufcg.computacao.eureca.backend.core.holders.*;
import br.edu.ufcg.computacao.eureca.backend.core.models.abstractions.Student;
import br.edu.ufcg.computacao.eureca.backend.core.models.mapentries.EurecaOperation;
import br.edu.ufcg.computacao.eureca.backend.core.models.mapentries.IdCode;
import br.edu.ufcg.computacao.eureca.backend.core.models.mapentries.StudentCourse;
import br.edu.ufcg.computacao.eureca.backend.core.plugins.AuthorizationPlugin;
import br.edu.ufcg.computacao.eureca.common.exceptions.ConfigurationErrorException;
import br.edu.ufcg.computacao.eureca.common.exceptions.EurecaException;
import br.edu.ufcg.computacao.eureca.common.util.CryptoUtil;
import br.edu.ufcg.computacao.eureca.common.util.ServiceAsymmetricKeysHolder;
import org.apache.log4j.Logger;

import java.security.GeneralSecurityException;

import java.security.interfaces.RSAPublicKey;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

public class ApplicationFacade {
    private static final Logger LOGGER = Logger.getLogger(ApplicationFacade.class);
    private RSAPublicKey asPublicKey;
    private AuthorizationPlugin authorizationPlugin;
    private static ApplicationFacade instance;

    private ApplicationFacade() {
    }

    public static ApplicationFacade getInstance() {
        synchronized (ApplicationFacade.class) {
            if (instance == null) {
                instance = new ApplicationFacade();
            }
            return instance;
        }
    }

    public void setAuthorizationPlugin(AuthorizationPlugin authorizationPlugin) {
        this.authorizationPlugin = authorizationPlugin;
    }

    public Collection<ActiveSummaryResponse> getActives(String token, String from, String to) throws EurecaException {
        authenticateAndAuthorize(token, EurecaOperation.GET_ACTIVES);
        Collection<ActiveSummaryResponse> activeStudentsSummary = new ArrayList<>();
        Collection<Student> actives = StudentStatisticsHolder.getInstance().getAllActives();
        actives.forEach(item -> {
            String admission = item.getAcademicData().getAdmission_term();
            if (admission != null && admission.compareTo(from) >= 0 && admission.compareTo(to) <= 0) {
                ActiveSummaryResponse studentSummary = new ActiveSummaryResponse(
                        item.getId().getRegistration(),
                        item.getAcademicData().getAdmission_term(),
                        item.getAcademicData().getTerms_count(),
                        computePercentage(item));
                activeStudentsSummary.add(studentSummary);
            }
        });
        return activeStudentsSummary;
    }

    public Collection<ActiveDataResponse> getActivesCSV(String token, String from, String to) throws EurecaException {
        authenticateAndAuthorize(token, EurecaOperation.GET_ACTIVES);
        Collection<ActiveDataResponse> activeStudentsData = new ArrayList<>();
        Collection<Student> actives = StudentStatisticsHolder.getInstance().getAllActives();
        actives.forEach(item -> {
            try {
                String admission = item.getAcademicData().getAdmission_term();
                if (admission != null && admission.compareTo(from) >= 0 && admission.compareTo(to) <= 0) {
                    ActiveDataResponse studentData = new ActiveDataResponse(item.getId().getRegistration(),
                            item.getPersonalData(), item.getAcademicData());
                    activeStudentsData.add(studentData);
                }
            } catch(Exception e) {
                e.printStackTrace();
            }
        });
        return activeStudentsData;
    }

    private double computePercentage(Student item) {
        StudentCourse data = item.getAcademicData();
        double totalCreditsFulfilled = data.getMandatory_credits() + data.getElective_credits() + data.getComplementary_credits();
        return totalCreditsFulfilled/Curriculum.totalCreditsNeeded;
    }

    public AlumniSummaryResponse getAlumni(String token, String from, String to) throws EurecaException {
        authenticateAndAuthorize(token, EurecaOperation.GET_ALUMNI);
        double accumulatedGPA = 0;
        int maxAlumniCount = 0;
        String maxAlumniCountTerm = "";
        int minAlumniCount = Integer.MAX_VALUE;
        String minAlumniCountTerm = "";
        int totalAlumniCount = 0;

        Collection<AlumniDataResponse> terms = getAlumniSummaryPerTerm(from, to);
        for (AlumniDataResponse item : terms) {
            double averageGPA = item.getAverage_gpa();
            int termAlumniCount = item.getAlumni_count();
            String term = item.getGraduation_term();
            totalAlumniCount += termAlumniCount;
            if (termAlumniCount >= maxAlumniCount) {
                maxAlumniCount = termAlumniCount;
                maxAlumniCountTerm = term;
            }
            if (termAlumniCount <= minAlumniCount) {
                minAlumniCount = termAlumniCount;
                minAlumniCountTerm = term;
            }
            accumulatedGPA += averageGPA * termAlumniCount;
        }

        AlumniSummaryResponse alumniSummaryResponse = new AlumniSummaryResponse(
                (totalAlumniCount == 0 ? -1.0 : accumulatedGPA/totalAlumniCount), maxAlumniCount,
                (terms.size() == 0 ? -1.0 : (1.0*totalAlumniCount)/terms.size()), minAlumniCount, minAlumniCountTerm,
                maxAlumniCountTerm, terms, totalAlumniCount);
        return alumniSummaryResponse;
    }

    public Collection<AlumniDataResponse> getAlumniCSV(String token, String from, String to) throws EurecaException {
        authenticateAndAuthorize(token, EurecaOperation.GET_ALUMNI_CSV);
        return getAlumniSummaryPerTerm(from, to);
    }

    private Collection<AlumniDataResponse> getAlumniSummaryPerTerm(String from, String to) {
        Collection<AlumniDataResponse> terms = new ArrayList<>();
        Map<String, Collection<String>> map = StudentStatisticsHolder.getInstance().getAlumniByGraduationTerm();
        for (Map.Entry<String, Collection<String>> entry : map.entrySet()) {
            String term = entry.getKey();
            if (term.compareTo(from) >= 0 && term.compareTo(to) <= 0) {
                Collection<String> cpfs = entry.getValue();
                int termAlumniCount = cpfs.size();
                double termAccumulatedGPA = 0;
                for (String cpf : cpfs) {
                    Student alumnus = StudentStatisticsHolder.getInstance().getAlumni().get(cpf);
                    termAccumulatedGPA += alumnus.getAcademicData().getGpa();
                }
                AlumniDataResponse termData = new AlumniDataResponse(termAccumulatedGPA/termAlumniCount, term,
                        termAlumniCount);
                terms.add(termData);
            }
        }
        return terms;
    }

    public Collection<DropoutSummaryResponse> getDropouts(String token, String from, String to) throws EurecaException {
        authenticateAndAuthorize(token, EurecaOperation.GET_DROPOUTS);
        Collection<DropoutSummaryResponse> dropoutSummaryResponses = new ArrayList<>();
        Map<String, Collection<String>> dropouts = StudentStatisticsHolder.getInstance().getDropoutByLeaveTerm();
        dropouts.forEach((k, v) -> {
            if (k.compareTo(from) >= 0 && k.compareTo(to) <= 0) {
                int dropoutsCount[] = new int[13];
                v.forEach(item -> {
                    Student dropout = StudentStatisticsHolder.getInstance().getDropouts().get(item);
                    dropoutsCount[dropout.getAcademicData().getDetailed_status_id()-1]++;
                });
                DropoutClassification dropoutClassification = new DropoutClassification(dropoutsCount[0],
                        dropoutsCount[12], dropoutsCount[1], dropoutsCount[2], dropoutsCount[3], dropoutsCount[4],
                        dropoutsCount[5], dropoutsCount[6], dropoutsCount[7], dropoutsCount[8]);
                dropoutSummaryResponses.add(new DropoutSummaryResponse(k, dropoutClassification));
            }
        });
        return dropoutSummaryResponses;
    }

    public Collection<DropoutDataResponse> getDropoutsCSV(String token, String from, String to) throws EurecaException {
        authenticateAndAuthorize(token, EurecaOperation.GET_DROPOUTS_CSV);
        Collection<DropoutDataResponse> dropoutDataResponses = new ArrayList<>();
        Map<String, Student> dropouts = StudentStatisticsHolder.getInstance().getDropouts();
        dropouts.forEach((k, v) -> {
            try {
                String leaveTerm = v.getAcademicData().getTerm_status();
                if (leaveTerm != null && leaveTerm.compareTo(from) >= 0 && leaveTerm.compareTo(to) <= 0) {
                    IdCode affirmativeActionId = new IdCode(v.getAcademicData().getAffirmative_action_id());
                    String affirmativeAction = MapsHolder.getInstance().getValue("Cota", affirmativeActionId).toString();
                    IdCode maritalStatusId = new IdCode(v.getPersonalData().getMarital_status_id());
                    String maritalStatus = MapsHolder.getInstance().getValue("EstadoCivil", maritalStatusId).toString();
                    IdCode genderId = new IdCode(v.getPersonalData().getGender_id());
                    String gender = MapsHolder.getInstance().getValue("Genero", genderId).toString();
                    IdCode idDropoutCause = new IdCode(v.getAcademicData().getDetailed_status_id());
                    String dropoutCause = MapsHolder.getInstance().getValue("SituacaoVinculo", idDropoutCause).toString();
                    DropoutDataResponse summary = new DropoutDataResponse(affirmativeAction, v.getAcademicData().getGpa(),
                            v.getAcademicData().getComplementary_credits(), v.getAcademicData().getMandatory_credits(),
                            v.getAcademicData().getElective_credits(), v.getAcademicData().getCurriculum(), maritalStatus,
                            gender, v.getAcademicData().getIea(), v.getId().getRegistration(), v.getAcademicData().getInstitutional_terms(),
                            v.getAcademicData().getMc(), v.getAcademicData().getAdmission_grade(),
                            v.getAcademicData().getMobility_terms(), dropoutCause, v.getAcademicData().getAdmission_term(),
                            v.getAcademicData().getTerms_count(), v.getAcademicData().getSuspended_terms());
                    dropoutDataResponses.add(summary);
                }
            } catch(Exception e) {
                e.printStackTrace();
            }
        });
        return dropoutDataResponses;
    }

    public Collection<AlumnusBasicData> getAlumniBasicData(String token) throws EurecaException {
        authenticateAndAuthorize(token, EurecaOperation.GET_ALUMNI_BASIC_DATA);
        Collection<AlumnusBasicData> alumniBasicData = new ArrayList<>();
        Map<String, Student> alumni = StudentStatisticsHolder.getInstance().getAlumni();
        alumni.forEach((k, v) -> {
            AlumnusBasicData basicData = new AlumnusBasicData(v.getId().getRegistration(), v.getPersonalData().getName(),
                    2, 1, v.getAcademicData().getAdmission_term(),
                    v.getAcademicData().getTerm_status());
            alumniBasicData.add(basicData);
        });
        return alumniBasicData;
    }

    public Map<String, Collection<SubjectSummaryResponse>> getSubjectSummary(String token, String from, String to) throws EurecaException {
        authenticateAndAuthorize(token, EurecaOperation.GET_SUBJECT_SUMMARY);
        Map<String, Collection<SubjectSummaryResponse>> completeMap = SubjectStatisticsHolder.getInstance().getSubjectSummary();
        Map<String, Collection<SubjectSummaryResponse>> resultMap = new HashMap<>();
        completeMap.forEach((term, summary) -> {
            if (term.compareTo(from) >= 0 && term.compareTo(to) <= 0) {
                resultMap.put(term, summary);
            }
        });
        return resultMap;
    }

    public String getPublicKey() throws EurecaException {
        try {
            return CryptoUtil.toBase64(ServiceAsymmetricKeysHolder.getInstance().getPublicKey());
        } catch (GeneralSecurityException e) {
            throw new ConfigurationErrorException(e.getMessage());
        }
    }

    private RSAPublicKey getAsPublicKey() throws EurecaException {
        if (this.asPublicKey == null) {
            this.asPublicKey = EurecaAsPublicKeyHolder.getInstance().getAsPublicKey();
        }
        return this.asPublicKey;
    }

    private SystemUser authenticateAndAuthorize(String token, EurecaOperation operation) throws EurecaException {
        // ToDo: remove this test when the frontend is updated to send the token in the request
        if (token == null || token.equals("")) return null;
        RSAPublicKey keyRSA = getAsPublicKey();
        SystemUser requester = AuthenticationUtil.authenticate(keyRSA, token);
        this.authorizationPlugin.isAuthorized(requester, operation);
        return requester;
    }

    public String getVersionNumber() {
        String buildNumber = null;
        buildNumber = PropertiesHolder.getInstance().getProperty(ConfigurationPropertyKeys.BUILD_NUMBER_KEY,
                    ConfigurationPropertyDefaults.BUILD_NUMBER);
        return SystemConstants.API_VERSION_NUMBER + "-" + buildNumber;
    }
}
