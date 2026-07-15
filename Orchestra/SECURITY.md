# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please send an email to the maintainers. All security vulnerabilities will be promptly addressed.

**Please do NOT report security vulnerabilities through public GitHub issues.**

### What to Include

When reporting a vulnerability, please include:

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Suggested fix (if any)
- Your contact information for follow-up

### Response Timeline

- **Acknowledgment:** Within 48 hours
- **Initial Assessment:** Within 1 week
- **Fix Released:** Depends on severity, typically within 2 weeks

## Security Best Practices

### API Keys

- **Never commit API keys** to version control
- Use environment variables or secret management
- Rotate keys regularly
- Use least-privilege access when possible

### Dependencies

- Regularly update dependencies
- Monitor for security advisories
- Use `pip-audit` to check for vulnerabilities:
  ```bash
  pip-audit
  ```

### Docker

- Use official, verified base images
- Run containers as non-root users
- Don't store secrets in Docker images
- Use multi-stage builds to reduce attack surface

### Database

- Use strong passwords
- Enable encryption in transit (SSL)
- Regularly backup data
- Restrict network access

### API Security

- Implement rate limiting
- Use API key authentication
- Validate all input data
- Return minimal error information in production
- Use HTTPS in production

## Known Security Considerations

### This Project

- **API Key Authentication:** The API uses `X-API-Key` header for authentication. In production, ensure the API key is strong and kept secret.

- **Database Credentials:** The default PostgreSQL credentials are for development only. Change them in production.

- **LLM API Keys:** OpenAI, Anthropic, and Tavily API keys are required for full functionality. Never commit these to version control.

- **CORS Configuration:** By default, CORS is configured for development (`localhost:3000`). Update `cors_origins` in production.

### Dependencies

This project uses several third-party libraries. While we keep dependencies updated, please:

1. Review `pyproject.toml` for current versions
2. Check for known vulnerabilities before deploying
3. Monitor security advisories for all dependencies

## Production Deployment

When deploying to production:

1. **Environment Variables**
   - Use a secrets manager (e.g., AWS Secrets Manager, HashiCorp Vault)
   - Never use default credentials
   - Enable environment variable encryption

2. **Network Security**
   - Use HTTPS/TLS
   - Implement proper firewall rules
   - Restrict database access to application servers

3. **Monitoring**
   - Enable logging and monitoring
   - Set up alerts for suspicious activity
   - Monitor API usage patterns

4. **Regular Maintenance**
   - Keep dependencies updated
   - Rotate secrets regularly
   - Review access logs

## Contact

For security-related questions or concerns, please contact the maintainers through:
- GitHub Issues (for general questions)
- Email (for security vulnerabilities)

We appreciate your help in keeping this project secure!
